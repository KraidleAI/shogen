"""Calibration E1, estimateur FIV_série SB-10a (E-S-38, E-S-39 ; T-FIV-1) : valeurs écrites à la main (série 1, 1, 0,
0 de la fixture de PLAN-S2BIS, scripts/plan-s2bis/tests/test_episodes.py l.36-44 ; série à lacune), chaînes d'EP
l.128 (γ̂₀ et σ̂²_bloc à ℓ = 1 ne dépendent que de n et K), et comptage naïf des γ̂_k depuis leur définition (paires de
la grille, écarts à Ī, en Fraction) sur des séries aléatoires à lacunes ; chaque test nomme les mutations qui le
rougissent."""
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
        cal = calib_fiv.calendrier_j28(calib_fiv.portee(TEXTE, PRM["calendrier"]), PRM["calendrier"])
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


class TestCritereE1(unittest.TestCase):
    def test_parametres_e1(self):
        """Section « e1 » : grille φ × κ × τ_D de 64 points dans l'ordre déclaré, 200 réplications par point, pool
        D1-bis (cible EP l.128-161), ℓ = 240 pour C1 ; source citée ; cellules E1-C0 et E1-<num>_<den>-<κ>-<τ_D>, φ =
        num/den irréductible (Q-T4-8, forme modifiée par l'avis, AVIS-SIM-T4.md l.56-59 : aucun « / », le nom de
        cellule nommant aussi les fichiers partiels de calcul, E-S-45) : 65 noms distincts, aucun « / ». Mutations
        M-10-28 (grille sans τ_D = 4 320), M-10-29 (cellule sans φ), M-14C-08 (« / » remis), M-14C-09 (séparateur
        « - »)."""
        g = calib_fiv.grille(PRM)
        self.assertEqual((len(g), g[0], g[1], g[-1]), (64, (Fraction(1, 100), 5, 60), (Fraction(1, 100), 5, 240),
                                                        (Fraction(1, 10), 50, 4320)))
        e = PRM["e1"]
        self.assertEqual((e["replications"], e["pool"], e["ell_c1"]), (200, "D1-bis", 240))
        self.assertTrue(all(x in e["source"] for x in ("E-S-38", "PROPOSITION l.197", "AVIS.md l.24")))
        self.assertEqual([calib_fiv.cellule(PRM, x) for x in (None, P1, (Fraction(1, 20), Fraction(10), 4320),
                                                              (Fraction(2, 100), Fraction(5), 240))],
                         ["E1-C0", "E1-1_100-5-60", "E1-1_20-10-4320", "E1-1_50-5-240"])
        noms = [calib_fiv.cellule(PRM, x) for x in [None] + g]
        self.assertEqual((len(set(noms)), [x for x in noms if "/" in x]), (65, []))

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
        """Grille réduite, cible EP fictive 1, 2 (gardés), 8 (non gardé) ; C0 : 1, 1, 1. P1 (1/100, 5, 60) : 1, 2, 4,
        critère 0 ; P2 (1/100, 50, 60) : 1, 2, 2, critère 0 ; P3 (1/10, 5, 60) : 1, 4, 3 ; P4 (1/10, 50, 60) : 1, 1, 1.
        C2 : égalité P1, P2 départagée par le plus petit κ : P1 ; C1 : moyenne de ln 1 et ln 4 = ln 2, P2 à distance 0 ;
        si P3 vaut aussi 2 à ℓ = 240, égalité P2, P3 : P3 (κ = 5). Critère de P3 : (ln 2)² (bc -l). Résidus de C2 :
        0, 0. P1 à FIV indéfini à un ℓ gardé : écarté, C2 = P2 ; P3 à 3/2 en 240 : C1 = P3 (|ln 1,5 − ln 2/2| =
        0,059, contre ln 2/2 pour P2 et P4) ; point manquant : E1/point ; FIV(240) de C0 indéfini : E1/indefini.
        Mutations M-10-33 (C2 au plus grand critère), M-10-34 (égalités au plus grand κ), M-10-35 (C1 sur la moyenne
        des FIV au lieu des log), M-10-36 (point indéfini compté pour 0)."""
        cible = [{"ell": e, "fiv": Fraction(x), "garde": g}
                 for e, x, g in ((1, 1, True), (2, 2, True), (240, 8, False))]
        moy = {None: m(1, 1, 1), P1: m(1, 2, 4), P2: m(1, 2, 2), P3: m(1, 4, 3), P4: m(1, 1, 1)}
        s = calib_fiv.selection(reduit(), {"calme": cible}, {p: {"calme": x} for p, x in moy.items()})["calme"]
        self.assertEqual((s["C2"], s["C1"], s["residus"]), (P1, P2, [0, 0]))
        self.assertLess(abs(s["criteres"][P3] - L22), EPS)
        moy[P3] = m(1, 4, 2)
        s = calib_fiv.selection(reduit(), {"calme": cible}, {p: {"calme": x} for p, x in moy.items()})["calme"]
        self.assertEqual((s["C2"], s["C1"]), (P1, P3))
        moy[P1], moy[P3] = m(1, None, 4), m(1, 4, Fraction(3, 2))     # P1 écarté de C2 ; C1 : ln 1,5 près de ln 2/2
        s = calib_fiv.selection(reduit(), {"calme": cible}, {p: {"calme": x} for p, x in moy.items()})["calme"]
        self.assertEqual((s["C2"], s["criteres"][P1], s["C1"]), (P2, None, P3))
        for faux, code in (({p: x for p, x in moy.items() if p != P4}, "E1/point"),
                           ({**moy, None: m(1, 1, None)}, "E1/indefini")):
            with self.assertRaises(commun.Refus) as c:
                calib_fiv.selection(reduit(), {"calme": cible}, {p: {"calme": x} for p, x in faux.items()})
            self.assertEqual(c.exception.code, code)

if __name__ == "__main__":
    unittest.main()
