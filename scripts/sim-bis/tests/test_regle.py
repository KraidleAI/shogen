"""Règle R1-2 répliquée, SB-7 et SB-8 (E-S-24 à E-S-35 ; T-ROT-1, T-ROT-2, T-REG-1 à T-REG-3, T-ABS-1) : décalages
calculés hors du code (`sha256sum`, puis `bc` en base 16, journal de la tranche 3 « vecteurs-t-rot-1.txt »), séries,
listes de K^(r) et décisions écrites à la main ; chaque test nomme les mutations qui le rougissent."""
import hashlib
import unittest
from fractions import Fraction
from unittest import mock

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

    def test_premiere_avant_absorption_q_t3_15(self):
        """Q-T3-15 (avis modifié, adjugé avant E0 ; ADR-0029 l.200) : l'unité non décalée est prise sur le pool BTC
        D1-bis restant après les retraits, avant le critère collectif d'absorption, et n'est pas recalculée après lui.
        À la main, n = 8 : binance {0, …, 5} (p̂ = 3/4), coinbase {0}, kraken {4} (1/8 chacun) ; premiere = binance ;
        filtrer retire binance (Σ p̂/(1 − p̂) = 3 + 2/7 > 1/2, puis 2/7). Valeurs « avec », R = 1, α = 1/2 (seuil 0),
        décalages de r = 1 en calme par sha256sum et bc (coinbase 1, kraken 4, modulo 8) : binance absente de la
        classe, toutes les unités sont décalées, comme sans unité non décalée (coinbase {1}, kraken {0} : K^(1) = 0,
        C1 = 0, causes k_crit et runs, K = 0) ; recalculée (coinbase non décalée : {0} et {0}, K^(1) = 1, C1 = 1), la
        garde changerait (runs seule). Mutation M-8F-06 (rotation : première unité présente non décalée quand
        `premier` manque)."""
        prm = dict(PRM, regle=dict(PRM["regle"], alpha=[1, 2]))
        btc = {"binance": bits(0, 1, 2, 3, 4, 5), "coinbase": bits(0), "kraken": bits(4)}
        premier = regle.premiere(list(btc))
        restees, retirees, indice = regle.filtrer(btc, 8, prm)
        self.assertEqual((premier, retirees, indice, restees), ("binance", ["binance"], Fraction(2, 7),
                                                                 {"coinbase": bits(0), "kraken": bits(4)}))
        t = {p: regle.tester(restees, p, G, "calme", 8, 10, prm, 1) for p in ("binance", None, "coinbase")}
        self.assertEqual(t["binance"], t[None])
        self.assertEqual([(t[p]["C1"], t[p]["causes"]) for p in ("binance", "coinbase")],
                         [(0, ["k_crit", "runs"]), (1, ["runs"])])

    def test_unites_series_nulles_e_s_28(self):
        """C-2 (b) de la G2 de la tranche 3 (E-S-28 ; ADR-0029 l.203 : au moins deux unités avec au moins un écart
        consolidé) : tester sur trois séries dont une seule non nulle (binance {0, 3} ; coinbase et kraken
        nulles), R = 1, α = 1/2 (seuil 0), n = 8, n_s = 10, à la main : unites = 1 (séries nulles non comptées), K = 0,
        aucun run ; aucune rotation calculée, K^(1) = 0 : C = 1, C1 = 0 → NON ÉVALUABLE, causes unites, k_crit et
        runs. Mutation V-22 du réviseur (unités comptées sur toutes les séries)."""
        prm = dict(PRM, regle=dict(PRM["regle"], alpha=[1, 2]))
        out = regle.tester({"binance": bits(0, 3), "coinbase": 0, "kraken": 0}, "binance", G, "calme", 8, 10, prm, 1)
        self.assertEqual((out["unites"], out["K"], out["runs"], out["C"], out["C1"], out["valeur"], out["causes"]),
                         (1, 0, 0, 1, 0, "NON ÉVALUABLE", ["unites", "k_crit", "runs"]))


HOTES = ["binance", "bitfinex", "bitstamp", "chainlink", "coinbase", "coingecko"]


def instance(i: int) -> tuple:
    """Instance d'essai i de T-REG-2 (flux « essai » de la cellule T-REG-2) : 3 à 5 unités, 120 à 239 fenêtres, écarts
    indépendants de part 1 à 11 %, et, une fois sur trois, deux incidents communs de 3 fenêtres sur 2 ou 3 unités."""
    u = aleas.flux(A, "T-REG-2", i, "essai", 0)
    n, nu, p = 120 + int(120 * u()), 3 + int(3 * u()), 0.01 + 0.1 * u()
    series = {h: sum(1 << t for t in range(n) if u() < p) for h in HOTES[:nu]}
    if u() < 1 / 3:
        for _j in range(2):
            t0, k = int((n - 3) * u()), 2 + int(2 * u())
            for h in HOTES[:k]:
                series[h] |= 7 << t0
    return series, n, aleas.graine_regle(A, "T-REG-2", i)


class TestModeComplet(unittest.TestCase):
    def test_mode_complet(self):
        """Mode à R complet (E-S-29), à la main : R = 9 (α = 1/2, seuil 4), K^(r) = 0, 1, 1, 2, 2, 3, 3, 3, 5 : #{≥ 1} =
        8, #{≥ 2} = 7, #{≥ 3} = 4 ≤ 4 (à la borne) → K_crit = 3 ; moyenne 20/9 ; K = 3 : C = 4 = seuil, REJETTE ; K = 2
        : C = 7, NE REJETTE PAS ; liste de 8 : REGLE/rotations. Mutations M-8A-01 (« ≥ » dans la recherche de K_crit),
        M-8A-02 (moyenne sur R + 1)."""
        prm = dict(PRM, regle=dict(PRM["regle"], alpha=[1, 2]))
        liste = ks([0, 1, 1, 2, 2, 3, 3, 3, 5])
        out = regle.complet(3, 2, 2, True, liste, 9, prm)
        self.assertEqual((out["valeur"], out["C"], out["C1"], out["K_crit"], out["moyenne"]),
                         ("REJETTE", 4, 8, 3, Fraction(20, 9)))
        self.assertEqual(regle.complet(2, 2, 2, True, liste, 9, prm)["valeur"], "NE REJETTE PAS")
        with self.assertRaises(commun.Refus) as c:
            regle.complet(3, 2, 2, True, liste[:8], 9, prm)
        self.assertEqual(c.exception.code, "REGLE/rotations")

    def test_arret_anticipe_t_reg_2(self):
        """T-REG-2, oracle exact (E-S-29) : 200 instances (R = 999, seuil 9), valeur et causes de l'arrêt anticipé
        égales à celles du mode à R complet, et cause k_crit ⇔ K_crit < 2 ; les instances couvrent REJETTE, NE REJETTE
        PAS et NON ÉVALUABLE, dont des arrêts avant R et la cause k_crit. S suivie (C-1 de la G2 de la tranche 3), sur
        les 60 premières : même valeur, mêmes causes et même réponse à « C_S ≤ seuil » dans les deux modes ; elles
        couvrent C_S ≤ 9 et C_S > 9, des arrêts et des passes complètes, dont une que seul C_S retient (C > 9, C1 > 9,
        C_S ≤ 9). oracle() rend le résultat anticipé et refuse un écart (REGLE/oracle ; désaccords forcés par
        mock.patch.object sur complet : causes seules ; S suivie, C_S passé de l'autre côté du seuil, instance 2).
        Mutations M-REG-6 (arrêt à C ≥ seuil), M-REG-7 (C1 non suivi), M-8A-03 (oracle sans comparaison des causes),
        M-8D-01 (oracle sans comparaison de C_S), M-8D-02 (C_S comparé à l'unité près, non par « ≤ seuil »)."""
        vus = set()
        for i in range(200):
            series, n, graine = instance(i)
            a, f = regle.deux_modes(series, "binance", graine, "calme", n, n, PRM, 999)
            self.assertEqual((a["valeur"], a["causes"]), (f["valeur"], f["causes"]), i)
            self.assertEqual("k_crit" in f["causes"], f["K_crit"] < 2, i)
            self.assertEqual(regle.oracle(series, "binance", graine, "calme", n, n, PRM, 999), a)
            vus |= {a["valeur"], "arrêt" if a["r"] < 999 else "complet"} | set(a["causes"])
        self.assertLessEqual({"REJETTE", "NE REJETTE PAS", "NON ÉVALUABLE", "arrêt", "complet", "k_crit"}, vus)
        vus = set()
        for i in range(60):
            series, n, graine = instance(i)
            a, f = regle.deux_modes(series, "binance", graine, "calme", n, n, PRM, 999, True)
            self.assertEqual((a["valeur"], a["causes"], a["C_S"] <= 9), (f["valeur"], f["causes"], f["C_S"] <= 9), i)
            self.assertEqual(regle.oracle(series, "binance", graine, "calme", n, n, PRM, 999, True), a)
            vus |= {"C_S ≤ 9" if a["C_S"] <= 9 else "C_S > 9", "arrêt" if a["r"] < 999 else "complet"}
            vus |= {"seul C_S"} if a["C"] > 9 and a["C1"] > 9 and a["C_S"] <= 9 else set()
        self.assertLessEqual({"C_S ≤ 9", "C_S > 9", "arrêt", "complet", "seul C_S"}, vus)
        vrai = regle.complet
        for j, avec_S, faux in ((0, False, lambda *x: dict(vrai(*x), causes=["k_crit"])),
                                (2, True, lambda *x: dict(vrai(*x), C_S=999 if vrai(*x)["C_S"] <= 9 else 0))):
            series, n, graine = instance(j)
            with mock.patch.object(regle, "complet", faux):
                with self.assertRaises(commun.Refus) as c:
                    regle.oracle(series, "binance", graine, "calme", n, n, PRM, 999, avec_S)
            self.assertEqual(c.exception.code, "REGLE/oracle", j)

    def test_sequence_et_f3_t_reg_3(self):
        """T-REG-3 (E-S-30, E-S-31 ; ADR-0029 l.204) : ETH (F2) testé seulement si BTC REJETTE dans la strate, sinon
        « NON TESTÉ (séquence) », son test sans condition gardé en diagnostic ; rejet familial (au moins un rejet, BTC
        puis ETH) ; USDC et USDT (F3) : valeur et causes du moteur, étiquette « exploratoire, hors décision », aucune
        valeur de registre. Mutations M-REG-8 (ETH toujours testé), M-8A-04 (F3 porté en registre)."""
        rj, nr = {"valeur": "REJETTE", "causes": []}, {"valeur": "NE REJETTE PAS", "causes": []}
        ne = {"valeur": "NON ÉVALUABLE", "causes": ["runs"]}
        s = regle.strate({"BTC": rj, "ETH": rj, "USDC": ne, "USDT": nr})
        self.assertEqual((s["ETH"]["valeur"], s["ETH"]["sans_condition"], s["familial"]), ("REJETTE", "REJETTE", True))
        self.assertEqual(s["USDC"], {"famille": "F3", "valeur": "NON ÉVALUABLE", "causes": ["runs"], "registre": None,
                                     "etiquette": "exploratoire, hors décision"})
        for btc in (nr, ne):
            s = regle.strate({"BTC": btc, "ETH": rj})
            e = s["ETH"]
            self.assertEqual((s["BTC"]["famille"], e["famille"], e["valeur"], e["sans_condition"], s["familial"]),
                             ("F1", "F2", "NON TESTÉ (séquence)", "REJETTE", False))
        self.assertEqual(regle.strate({"BTC": rj, "ETH": nr})["familial"], True)


class TestEvenementsEtAbsorption(unittest.TestCase):
    def test_evenements_e_s_34(self):
        """Compte d'événements (E-S-34 ; tolérances g de regle.tolerances, recopiées : 0, 5, 20, 60), à la main sur la
        suite comprimée de 40 positions, I = {0, 1, 3, 10, 11, 30} : g = 0 → 4 runs ; g = 1 (un 0 entre 1 et 3) → 3 ;
        g = 5 → 3 ; g = 6 (six 0 entre 3 et 10) → 2 ; g = 18 → 1 ; I = {0, 39}, g = 0 → 2 (suite linéaire, aucun
        enroulement). Loi de rotation (R = 1, α = 1/2, mêmes décalages que test_tester_rotation_r_1) : binance {0, 3},
        coinbase {0, 3, 7} : E = 2 à g = 0, 1 à g = 5 ; rotation r = 1 : I = {0}, E^(1) = 1 ; C = 0 à g = 0, 1 à g = 5 ;
        queue basse (Q-T3-13, avis modifié) : C_bas = #{r : E^(r) ≤ E} = 1 aux deux g. Mutations M-8B-01 (tolérance
        g + 1), M-8B-02 (tolérance g − 1), M-8B-03 (tolérance ignorée), M-8F-03 (queue basse omise)."""
        self.assertEqual(PRM["regle"]["tolerances"], [0, 5, 20, 60])
        i = bits(0, 1, 3, 10, 11, 30)
        self.assertEqual([regle.evenements(i, g, 40) for g in (0, 1, 5, 6, 18)], [4, 3, 3, 2, 1])
        self.assertEqual(regle.evenements(bits(0, 39), 0, 40), 2)
        prm = dict(PRM, regle=dict(PRM["regle"], alpha=[1, 2], tolerances=[0, 5]))
        loi = regle.loi_evenements({"binance": bits(0, 3), "coinbase": bits(0, 3, 7)}, "binance", G, "calme", 8, 1,
                                   prm)
        self.assertEqual(loi, {0: {"E": 2, "C": 0, "C_bas": 1}, 5: {"E": 1, "C": 1, "C_bas": 1}})

    def test_loi_evenements_oracle_q_t3_13(self):
        """Q-T3-13 (avis modifié, adjugé avant E0) : loi de rotation du compte d'événements, deux queues, contre un
        oracle naïf écrit ici : décalages refaits par hashlib (SHA-256 de « <graine>:calme:<r>:<u> », big-endian, modulo
        n ; binance non décalée), rotation position par position (la valeur de t va en (t + o) mod n), I_t = 1{m_t ≥ 2},
        événements sur la suite linéaire (un 1 ouvre un événement si plus de g zéros le séparent du 1 précédent). 30
        instances de T-REG-2, R = 40, g ∈ {0 ; 5 ; 20 ; 60} : E, C = #{r : E^(r) ≥ E} et C_bas = #{r : E^(r) ≤ E}
        égaux ; les instances ont des C strictement entre 0 et R et égaux à R, des C_bas à 0, strictement entre 0 et
        R et égaux à R. Mutations M-8F-03
        (queue basse omise), M-8F-04 (« < » dans la queue basse), M-8F-05 (queue basse comptée sur E^(r) ≥ E)."""
        def evts(i, g):
            e, dernier = 0, None
            for t, x in enumerate(i):
                if x:
                    e, dernier = e + (dernier is None or t - dernier - 1 > g), t
            return e

        def masque_i(series, graine, n, r):
            m = [0] * n
            for u, x in series.items():
                h = hashlib.sha256(f"{graine}:calme:{r}:{u}".encode("ascii")).digest()
                o = 0 if r == 0 or u == "binance" else int.from_bytes(h, "big") % n
                for t in range(n):
                    m[(t + o) % n] += x >> t & 1
            return [int(v >= 2) for v in m]
        vus, gs = set(), PRM["regle"]["tolerances"]
        for k in range(30):
            series, n, graine = instance(k)
            obs = {g: evts(masque_i(series, graine, n, 0), g) for g in gs}
            rot = [masque_i(series, graine, n, r) for r in range(1, 41)]
            attendu = {g: {"E": obs[g], "C": sum(evts(i, g) >= obs[g] for i in rot),
                           "C_bas": sum(evts(i, g) <= obs[g] for i in rot)} for g in gs}
            self.assertEqual(regle.loi_evenements(series, "binance", graine, "calme", n, 40, PRM), attendu, k)
            vus |= {(q, "0" if x[q] == 0 else "R" if x[q] == 40 else "entre") for x in attendu.values()
                    for q in ("C", "C_bas")}
        self.assertLessEqual({("C", "entre"), ("C", "R"), ("C_bas", "0"), ("C_bas", "entre"), ("C_bas", "R")}, vus)

    def test_absorption_t_abs_1(self):
        """T-ABS-1 (E-S-35 ; c* = 1/2 recopié) : pool de 5 unités à p̂ écrits à la main, a 1/2, b 1/4, c 1/10, d 1/10, e
        1/20 : Σ p̂/(1 − p̂) = 1 + 1/3 + 1/9 + 1/9 + 1/19 = 275/171 > 1/2 → a retirée ; 104/171 > 1/2 → b ; 47/171 ≤ 1/2
        : arrêt, retirées a, b, indice 47/171. Égalité (x et y à 1/3, z à 1/10) : x puis y (nom croissant), indice 1/9.
        Indice égal à c* (u à 1/3 : 1/2) : rien retiré. p̂ = 1 : indice infini, retirée d'abord. Séries (n = 20) : a 10
        écarts, b 5, c 2, d 2, e 1 → restent c, d, e. Mutations M-ABS-1 (retrait par p̂ croissant), M-8B-04 (« ≥ c* »),
        M-8B-05 (indice Σ p̂ sans 1 − p̂), M-8B-06 (égalité départagée par nom décroissant)."""
        f = Fraction
        self.assertEqual(PRM["regle"]["c_etoile"], [1, 2])
        p = {"a": f(1, 2), "b": f(1, 4), "c": f(1, 10), "d": f(1, 10), "e": f(1, 20)}
        self.assertEqual(regle.absorption(p, f(1, 2)), (["a", "b"], f(47, 171)))
        self.assertEqual(regle.absorption({"y": f(1, 3), "x": f(1, 3), "z": f(1, 10)}, f(1, 2)), (["x", "y"], f(1, 9)))
        self.assertEqual(regle.absorption({"u": f(1, 3)}, f(1, 2)), ([], f(1, 2)))
        self.assertEqual(regle.absorption({"u": f(1), "v": f(1, 10)}, f(1, 2)), (["u"], f(1, 9)))
        series = {"a": (1 << 10) - 1, "b": (1 << 5) - 1, "c": 3, "d": 3, "e": 1}
        self.assertEqual(regle.filtrer(series, 20, PRM), ({"c": 3, "d": 3, "e": 1}, ["a", "b"], f(47, 171)))


G6 = "6fce4df75bac7db6ff01817b407f6331e49ec2ebf31f02e6672d3ab8a3bc9688"  # printf … SHOGEN-RB6-VECTEURS | sha256sum


class TestContratRB6(unittest.TestCase):
    def test_vecteurs_du_contrat_rb6(self):
        """Contrat de rotation de RB-6 (docs/adr-0029/s2bis/ROTATION-S2BIS.md §2 et §5, diffs RB-6a et RB-6b, en
        relecture G2) : ses six vecteurs o(r, u), recalculés par sha256sum et bc (journal de la tranche 3
        « vecteurs-rb6.txt »), noms d'hôte de configuration compris, dont o = 0 et o = n − 1, et la même entrée sous n
        et n/2 ; ses huit masques décalés à la main (la valeur de la position t va en (t + o) mod n) ; ses libellés de
        strate, égaux à calibration.strates. Mutations M-8C-01 (unité réduite aux lettres et chiffres), M-8C-02 (strates
        du contrat autres que calibration.strates)."""
        for s, r, u, n, o in (("calme", 1, "api.binance.com", 109440, 107527),
                              ("stress", 9999, "ethereum-rpc.publicnode.com", 43776, 24225),
                              ("calme", 4242, "api.kraken.com", 54720, 39743), ("calme", 1, "api.coinbase.com", 7, 0),
                              ("calme", 7, "api.coinbase.com", 7, 6), ("calme", 1, "api.binance.com", 54720, 52807)):
            self.assertEqual(regle.decalage(G6, s, r, u, n), o, (s, r, u, n))
        tous = bits(0, 1, 2, 3, 4)
        for m, o, n, attendu in ((bits(0, 3, 6), 2, 7, bits(1, 2, 5)), (bits(0, 3, 6), 6, 7, bits(2, 5, 6)),
                                 (bits(0, 3, 6), 0, 7, bits(0, 3, 6)), (bits(4), 1, 5, bits(0)),
                                 (bits(0), 3, 5, bits(3)), (tous, 4, 5, tous), (0, 3, 5, 0), (bits(0), 0, 1, bits(0))):
            self.assertEqual(regle.tourner(m, o, n), attendu, (m, o, n))
        self.assertEqual(list(regle.STRATES), PRM["calibration"]["strates"])

    def test_refus_du_contrat_rb6(self):
        """Refus nommés du contrat RB-6 (§1 et §4), avant tout calcul. decalage : strate hors de calme et stress
        (REGLE/libelle) ; r au-delà de 9 999, booléen ou chaîne, n booléen (REGLE/entier) ; graine en octets ou de 65
        caractères (REGLE/graine) ; unité vide, avec « : », DEL ou tabulation (REGLE/libelle) ; « ! » précédé d'une
        espace et « ~ », bornes ASCII imprimables admises jusqu'à P-7, refusés (REGLE/libelle ; test_noms_d_unite_p_7).
        seuil : R au-delà de 9 999 (REGLE/seuil, α = 1/2). tester,
        loi_evenements et filtrer contrôlent toutes leurs entrées, même quand aucune rotation n'est calculée (une seule
        série non nulle, ou unité non décalée seule) : graine (REGLE/graine), n nul (REGLE/entier), nom d'unité ou unité
        non décalée hors du contrat (REGLE/libelle), masque négatif, booléen ou au-delà de n bits (REGLE/masque), R de
        loi_evenements au-delà de 9 999 et n booléen de filtrer (REGLE/entier). Mutations M-8C-03 à M-8C-15."""
        def refus(code, f, *a):
            with self.subTest(code=code, f=f.__name__, a=a):
                with self.assertRaises(commun.Refus) as c:
                    f(*a)
                self.assertEqual(c.exception.code, code)
        for code, a in (("REGLE/libelle", (G6, "crise", 1, "a", 7)), ("REGLE/libelle", (G6, "Calme", 1, "a", 7)),
                        ("REGLE/entier", (G6, "calme", 10000, "a", 7)), ("REGLE/entier", (G6, "calme", True, "a", 7)),
                        ("REGLE/entier", (G6, "calme", "01", "a", 7)), ("REGLE/entier", (G6, "calme", 1, "a", True)),
                        ("REGLE/graine", (bytes.fromhex(G6), "calme", 1, "a", 7)),
                        ("REGLE/graine", (G6 + "0", "calme", 1, "a", 7)), ("REGLE/libelle", (G6, "calme", 1, "", 7)),
                        ("REGLE/libelle", (G6, "calme", 1, "a:4", 7)),
                        ("REGLE/libelle", (G6, "calme", 1, "a" + chr(127), 7)),
                        ("REGLE/libelle", (G6, "calme", 1, "a" + chr(9) + "b", 7)),
                        ("REGLE/libelle", (G6, "calme", 9999, " !", 1)),
                        ("REGLE/libelle", (G6, "calme", 9999, "~", 1))):
            refus(code, regle.decalage, *a)
        refus("REGLE/seuil", regle.seuil, 10001, [1, 2])
        self.assertEqual(regle.seuil(9999, [1, 2]), 4999)
        for code, series, premier, g, n in (("REGLE/graine", {"a": 1, "b": 0}, "a", G6.upper(), 3),
                                            ("REGLE/entier", {"a": 0}, None, G6, 0),
                                            ("REGLE/libelle", {"a:b": 1}, None, G6, 3),
                                            ("REGLE/libelle", {"a": 1, "a:b": 2}, "a:b", G6, 3),
                                            ("REGLE/libelle", {"a": 1}, "", G6, 3),
                                            ("REGLE/masque", {"a": 8}, None, G6, 3),
                                            ("REGLE/masque", {"a": -1}, None, G6, 3),
                                            ("REGLE/masque", {"a": True, "b": 1}, "b", G6, 3)):
            refus(code, regle.tester, series, premier, g, "calme", n, 3, PRM, 9999)
            refus(code, regle.loi_evenements, series, premier, g, "calme", n, 9, PRM)
        refus("REGLE/entier", regle.loi_evenements, {"a": 1}, "a", G6, "calme", 3, 10000, PRM)
        for code, series in (("REGLE/masque", {"a": 8}), ("REGLE/masque", {"a": -1}), ("REGLE/masque", {"a": True})):
            refus(code, regle.filtrer, series, 3, PRM)
        refus("REGLE/entier", regle.filtrer, {"a": 1}, True, PRM)

    def test_noms_d_unite_p_7(self):
        """P-7 de l'avis de la tranche 3 (adjugé avant E0, comme Q-RB-13 adoptée pour RB-6) : noms d'unité aux seuls
        caractères d'un nom d'hôte, en minuscules (lettres a à z, chiffres, « - », « . »), 1 à 253 caractères ; refus
        REGLE/libelle par _cle et ses appelants : decalage, et tester, deux_modes, oracle et loi_evenements par
        _controler, unité non décalée comprise. Admis : les dix noms courts du pool, les noms d'hôte du contrat RB-6
        (api-pub.bitfinex.com, ethereum-rpc.publicnode.com), 253 caractères. Refusés : « ! » précédé d'une espace et
        « ~ » (admis jusqu'ici), majuscule, « _ », espace, 254 caractères, octets. Mutations M-8E-01 (majuscules
        admises), M-8E-02 (borne de 253 retirée), M-8E-03 (« _ » admis), M-8E-04 (unités non contrôlées par
        _controler), M-8E-05 (unité non décalée non contrôlée)."""
        def code(f, *a):
            try:
                f(*a)
                return None
            except commun.Refus as e:
                return e.code
        admis = [h for h, _f in PRM["calibration"]["unites"]] + ["api-pub.bitfinex.com", "ethereum-rpc.publicnode.com",
                                                                  "a" * 253]
        self.assertEqual([code(regle.decalage, G6, "calme", 1, u, 7) for u in admis], [None] * 13)
        refuses = [" !", "~", "Binance", "okx_ticker", "a b", "a" * 254, b"okx"]
        self.assertEqual([code(regle.decalage, G6, "calme", 1, u, 7) for u in refuses], ["REGLE/libelle"] * 7)
        cas = (({"Binance": 1, "okx": 2}, "okx"), ({"binance": 1, "okx": 2}, "~"))
        for f in (regle.tester, regle.deux_modes, regle.oracle):
            self.assertEqual([code(f, s, p, G6, "calme", 3, 3, PRM, 99) for s, p in cas], ["REGLE/libelle"] * 2)
        self.assertEqual([code(regle.loi_evenements, s, p, G6, "calme", 3, 9, PRM) for s, p in cas],
                         ["REGLE/libelle"] * 2)
