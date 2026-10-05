"""Règle R1-2 répliquée, SB-7 et SB-8 (E-S-24 à E-S-35 ; T-ROT-1, T-ROT-2, T-REG-1 à T-REG-3, T-ABS-1) : décalages
calculés hors du code (`sha256sum`, puis `bc` en base 16, journal de la tranche 3 « vecteurs-t-rot-1.txt »), séries,
listes de K^(r) et décisions écrites à la main ; chaque test nomme les mutations qui le rougissent."""
import unittest

import aleas
import commun
import regle

PRM = commun.charger_parametres(environ={})
A = PRM["aleas"]
G = "26455ac198150c505226ead3117413190f3c1639660290a216bee811e157e0b2"   # printf … T-ROT-1|0 | sha256sum


def bits(*positions) -> int:
    m = 0
    for p in positions:
        m |= 1 << p
    return m


class TestRotation(unittest.TestCase):
    def refus(self, code, f, *a):
        with self.assertRaises(commun.Refus) as c:
            f(*a)
        self.assertEqual(c.exception.code, code)

    def test_decalages_t_rot_1(self):
        """T-ROT-1 : o(r, u) = entier big-endian des 32 octets de SHA-256 de « <graine>:<strate>:<r>:<u> » modulo n
        (E-S-27 ; AVIS-C Q-R-02) ; graine de règle de la réplication (T-ROT-1, 0) recalculée par sha256sum (E-S-41) ;
        cinq vecteurs par sha256sum et bc, dont o = 0 (gemini, n = 7) et o = n − 1 (bitstamp, n = 19). Graine non
        hexadécimale minuscule de 64 caractères : REGLE/graine ; « : » ou caractère hors ASCII imprimable dans la strate
        ou l'unité : REGLE/libelle ; r ou n nul : REGLE/entier. Mutations M-ROT-1 (classe dans l'entrée), M-7A-01 (huit
        premiers octets seulement), M-7A-02 (petit-boutiste), M-7A-03 (séparateur « | »), M-7A-04 (graine non
        contrôlée), M-7A-05 (libellés non contrôlés), M-7A-06 (r sur quatre chiffres)."""
        self.assertEqual(aleas.graine_regle(A, "T-ROT-1", 0), G)
        for s, r, u, n, o in (("calme", 1, "kraken", 109440, 38692), ("stress", 9999, "binance", 43776, 21459),
                              ("calme", 10, "okx", 24585, 4167), ("stress", 2, "gemini", 7, 0),
                              ("calme", 3, "bitstamp", 19, 18)):
            self.assertEqual(regle.decalage(G, s, r, u, n), o, (s, r, u))
        for code, a in (("REGLE/graine", (G.upper(), "calme", 1, "okx", 7)),
                        ("REGLE/graine", (G[1:], "calme", 1, "okx", 7)), ("REGLE/libelle", (G, "cal:me", 1, "okx", 7)),
                        ("REGLE/libelle", (G, "calme", 1, "okx" + chr(233), 7)),
                        ("REGLE/entier", (G, "calme", 0, "okx", 7)), ("REGLE/entier", (G, "calme", 1, "okx", 0))):
            self.refus(code, regle.decalage, *a)

    def test_sens_de_rotation(self):
        """Sens fixé (AVIS-C Q-R-02) : la valeur de la position t va en (t + o) mod n. n = 8 : positions 0, 1 décalées
        de 3 → 3, 4 ; positions 6, 7 → 1, 2 (enroulement) ; o = 0 : inchangé. Mutation M-ROT-4 : sens inversé."""
        self.assertEqual([regle.tourner(bits(0, 1), 3, 8), regle.tourner(bits(6, 7), 3, 8),
                          regle.tourner(bits(0, 2), 0, 8)], [bits(3, 4), bits(1, 2), bits(0, 2)])

    def test_k_et_s_t_rot_2(self):
        """T-ROT-2, à la main, trois unités sur 8 fenêtres : A = {0, 1, 4}, B = {1, 2, 4}, C = {4, 7} : m = 1, 2, 1, 0,
        3, 0, 0, 1 → K = 2 (fenêtres 1 et 4), S = C(2, 2) + C(3, 2) = 4. B décalée de 1 ({2, 3, 5}), C de 6 ({2, 5}) : K
        = 2 (2 et 5), S = 2. B de 7 ({0, 1, 3}), C de 1 ({0, 5}) : m = 3, 2, 0, 1, 1, 1 → K = 2 (0 et 1), S = 4. Puis 1
        000 essais aléatoires (2 à 10 unités, 1 à 64 fenêtres) : K et S égaux au comptage naïf position par position.
        Mutations M-ROT-5 (« au moins un »), M-ROT-6 (S sans le terme croisé des plans), M-7A-07 (coefficient d'un plan
        sans la division par 2)."""
        a, b, c = bits(0, 1, 4), bits(1, 2, 4), bits(4, 7)
        cas = [([a, b, c], bits(1, 4), 4), ([a, regle.tourner(b, 1, 8), regle.tourner(c, 6, 8)], bits(2, 5), 2),
               ([a, regle.tourner(b, 7, 8), regle.tourner(c, 1, 8)], bits(0, 1), 4)]
        for series, i, s in cas:
            self.assertEqual((regle.deux(series), regle.paires(series)), (i, s))
        for k in range(1000):
            u = aleas.flux(A, "T-ROT-2", k, "essai", 0)
            n, nu = 1 + int(64 * u()), 2 + int(9 * u())
            series = [sum(1 << t for t in range(n) if u() < 0.3) for _j in range(nu)]
            m = [sum(x >> t & 1 for x in series) for t in range(n)]
            self.assertEqual((regle.deux(series).bit_count(), regle.paires(series)),
                             (sum(1 for v in m if v >= 2), sum(v * (v - 1) // 2 for v in m)), k)
        with self.assertRaises(commun.Refus) as e:
            regle.paires([1] * 16)
        self.assertEqual(e.exception.code, "REGLE/plans")
        self.assertEqual(regle.paires([1] * 15), 105)


def ks(*listes) -> list:
    """K^(r) injectés, r = 1, 2, … (S non suivie)."""
    return [(k, None) for liste in listes for k in liste]


class TestDecision(unittest.TestCase):
    def test_parametres_et_seuil(self):
        """Section regle recopiée à la main (ADR-0029 l.139, l.200-203 ; AVIS Q-S-06 complément 1) : R = 9 999, R = 999
        pour la grille et l'absorption, α = 1/100, garde (deux unités en écart, K_crit ≥ 2, deux runs). Seuil entier
        α·(R + 1) − 1 : 99 à R = 9 999, 9 à R = 999 ; R = 9 998 : REGLE/seuil. Mutation M-REG-4 (R + 1 → R)."""
        r = PRM["regle"]
        self.assertEqual((r["R"], r["R_approche"], r["alpha"], r["garde"]),
                         (9999, 999, [1, 100], {"unites": 2, "k_crit": 2, "runs": 2}))
        self.assertEqual([regle.seuil(9999, [1, 100]), regle.seuil(999, [1, 100])], [99, 9])
        with self.assertRaises(commun.Refus) as c:
            regle.seuil(9998, [1, 100])
        self.assertEqual(c.exception.code, "REGLE/seuil")

    def test_retraits_e_s_24(self):
        """D1-bis et flux presque mort par classe, avant K (E-S-24 ; ADR-0029 l.170), à la main, n = 10 en calme et 6 en
        stress : u1 (10, 6) reste ; u2 (0, 0) : D1-bis (a) dans les deux strates ; u3 (0, 3) : D1-bis (b) en calme,
        reste en stress (2·3 = 6) ; u4 (4, 2) : presque mort dans les deux (8 < 10, 4 < 6) ; u5 (5, 3) reste (2·ok = n).
        Mutations M-7B-01 (« ≤ » au lieu de « < »), M-7B-02 (D1-bis (a) non distinguée), M-7B-03 (seuil de flux
        presque mort omis)."""
        ok = {("u1", "calme"): 10, ("u1", "stress"): 6, ("u2", "calme"): 0, ("u2", "stress"): 0, ("u3", "calme"): 0,
              ("u3", "stress"): 3, ("u4", "calme"): 4, ("u4", "stress"): 2, ("u5", "calme"): 5, ("u5", "stress"): 3}
        self.assertEqual(regle.retraits(ok, {"calme": 10, "stress": 6}),
                         {("u2", "calme"): "D1-bis (a)", ("u2", "stress"): "D1-bis (a)", ("u3", "calme"): "D1-bis (b)",
                          ("u4", "calme"): "presque mort", ("u4", "stress"): "presque mort"})

    def test_decision_t_reg_1(self):
        """T-REG-1, listes de K^(r) injectées (R = 9 999, seuil 99), K = 3, deux runs, deux unités, n′ suffisant : 99
        valeurs ≥ 3 → C = 99, REJETTE ; 100 → C = 100 (arrêt à r = 100), NE REJETTE PAS. K = 1 : C1 = 99 → NON
        ÉVALUABLE (k_crit) ; K = 2, C1 = 100 et C = 0 → REJETTE. Un run → NON ÉVALUABLE (runs) ; une unité (unites) ;
        n′ < n_s/2 (n_prime). Arrêt : 100 fois K = 1, puis 99 fois K = 3 (C = 99 à r = 199), 0, 3 : pas d'arrêt avant
        C = 100, en r = 201. K = 0 : C1 n'atteint 100 qu'à r = 299, garde tenue (seule cause : runs). R = 999
        (seuil 9, garde C1 ≥ 10) : 9 valeurs ≥ 3 puis 990 fois 1 → REJETTE ; 10 → NE REJETTE PAS. Liste trop courte :
        REGLE/rotations. S suivie (S = 5) : 100 fois (3, 5) → C_S = 100, arrêt à r = 100 ; (3, 4) → C_S = 0, pas
        d'arrêt (E-S-29 : et C_S > seuil quand S est suivie). Mutations M-REG-1 (C < seuil), M-REG-2 (garde C1 ≥ 1),
        M-REG-3 (un run suffit), M-REG-5 (« > » au lieu de « ≥ » dans C), M-REG-6 (arrêt à C ≥ seuil), M-REG-7 (C1
        non suivi), M-7B-04 (unités non comptées), M-7B-07 (« > » dans C_S)."""
        def d(k, runs, unites, suffisant, liste, R=9999):
            self.assertEqual(len(liste), R)
            out = regle.decider(k, runs, unites, suffisant, liste, R, PRM)
            return out["valeur"], out["causes"], out["C"], out["r"]
        self.assertEqual(d(3, 2, 2, True, ks([3] * 99, [2] * 9900)), ("REJETTE", [], 99, 9999))
        self.assertEqual(d(3, 2, 2, True, ks([3] * 100, [0] * 9899)), ("NE REJETTE PAS", [], 100, 100))
        self.assertEqual(d(1, 2, 2, True, ks([1] * 99, [0] * 9900))[:2], ("NON ÉVALUABLE", ["k_crit"]))
        self.assertEqual(d(2, 2, 2, True, ks([1] * 100, [0] * 9899)), ("REJETTE", [], 0, 9999))
        self.assertEqual(d(3, 1, 2, True, ks([3] * 99, [2] * 9900))[:2], ("NON ÉVALUABLE", ["runs"]))
        self.assertEqual(d(3, 2, 1, True, ks([3] * 99, [2] * 9900))[:2], ("NON ÉVALUABLE", ["unites"]))
        self.assertEqual(d(3, 2, 2, False, ks([3] * 99, [2] * 9900))[:2], ("NON ÉVALUABLE", ["n_prime"]))
        self.assertEqual(d(3, 2, 2, True, ks([1] * 100, [3] * 99, [0], [3], [0] * 9798)),
                         ("NE REJETTE PAS", [], 100, 201))
        self.assertEqual(d(0, 0, 2, True, ks([0] * 199, [1] * 9800))[:2], ("NON ÉVALUABLE", ["runs"]))
        self.assertEqual(d(3, 2, 2, True, ks([3] * 9, [1] * 990), 999), ("REJETTE", [], 9, 999))
        self.assertEqual(d(3, 2, 2, True, ks([3] * 10, [1] * 989), 999), ("NE REJETTE PAS", [], 10, 10))
        s = regle.decider(3, 2, 2, True, [(3, 5)] * 100 + [(0, 0)] * 9899, 9999, PRM, 5)
        self.assertEqual((s["valeur"], s["C_S"], s["r"]), ("NE REJETTE PAS", 100, 100))
        s = regle.decider(3, 2, 2, True, [(3, 4)] * 100 + [(0, 0)] * 9899, 9999, PRM, 5)
        self.assertEqual((s["valeur"], s["C"], s["C_S"], s["r"]), ("NE REJETTE PAS", 100, 0, 9999))
        with self.assertRaises(commun.Refus) as c:
            regle.decider(3, 2, 2, True, ks([3] * 99, [2] * 9899), 9999, PRM)
        self.assertEqual(c.exception.code, "REGLE/rotations")

    def test_tester_rotation_r_1(self):
        """Chemin complet à R = 1 (α = 1/2 en paramètre d'essai : seuil 0), n = 8, n_s = 10, binance (non décalée),
        coinbase et kraken ; décalages de r = 1 en calme par sha256sum et bc : coinbase 1, kraken 4 (modulo 8 ; modulo
        10 : 1 et 2). A : {0}, {7}, {2} → tournées {0}, {0}, {6} : K^(1) = 1, C1 = 1, garde tenue, seule cause runs
        (K = 0) ; toutes décalées (unité non décalée absente de la classe, binance de 1) : K^(1) = 0, causes k_crit et
        runs. B : {0}, {5}, {2} → {0}, {6}, {6} : K^(1) = 1. C : {0, 3}, {0, 3, 7}, {} → K = 2 en deux runs ; coinbase
        {1, 4, 0} : K^(1) = 1, C = 0, C1 = 1 → REJETTE ; n_s = 16 (2·8 = 16) : REJETTE ; n_s = 17 : NON ÉVALUABLE
        (n_prime). S suivie en C : S = 2 (fenêtres 0 et 3), S^(1) = 1, C_S = 0. Mutations M-ROT-2 (unité non décalée
        décalée), M-ROT-3 (modulo n_s au lieu de n′_s), M-7B-05 (« > » dans n′_s ≥ n_s/2), M-7B-06 (dernier hôte non
        décalé), M-7B-08 (S non suivie)."""
        prm = dict(PRM, regle=dict(PRM["regle"], alpha=[1, 2]))

        def t(b, c, k, premier="binance", n_s=10):
            out = regle.tester({"binance": b, "coinbase": c, "kraken": k}, premier, G, "calme", 8, n_s, prm, 1)
            return out["valeur"], out["causes"], out["C1"]
        self.assertEqual(t(bits(0), bits(7), bits(2)), ("NON ÉVALUABLE", ["runs"], 1))
        self.assertEqual(t(bits(0), bits(7), bits(2), None), ("NON ÉVALUABLE", ["k_crit", "runs"], 0))
        self.assertEqual(t(bits(0), bits(5), bits(2)), ("NON ÉVALUABLE", ["runs"], 1))
        self.assertEqual(t(bits(0, 3), bits(0, 3, 7), 0), ("REJETTE", [], 1))
        self.assertEqual([t(bits(0, 3), bits(0, 3, 7), 0, n_s=16), t(bits(0, 3), bits(0, 3, 7), 0, n_s=17)],
                         [("REJETTE", [], 1), ("NON ÉVALUABLE", ["n_prime"], 1)])
        out = regle.tester({"binance": bits(0, 3), "coinbase": bits(0, 3, 7)}, "binance", G, "calme", 8, 10, prm, 1,
                           True)
        self.assertEqual((out["S"], out["C_S"], out["K"], out["runs"], out["unites"]), (2, 0, 2, 2, 2))
        self.assertEqual(regle.premiere(["kraken", "binance", "okx"]), "binance")
        self.assertIsNone(regle.premiere([]))
