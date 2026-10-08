"""Calibration SB-2 (E-S-37, E-S-02 ; T-CAL-1) : EP l.13, l.14, l.140 et l.144 recopiées à la main, nombres pris en
`Fraction` depuis leur écriture décimale ; une retouche par contrôle de forme et de cohérence ; chaque test nomme les
mutations qui le rougissent. Contrôle hors code : `bc` donne 372/24585 = 0,0151311775472849298352654057352043929225137
278828553… et 372/332 = 1,12048192771084337349397590361445783132530120481927710…, dont les 50 chiffres significatifs
arrondis au plus proche sont les valeurs imprimées par EP l.13."""
import unittest
from fractions import Fraction

import calib_fiv
import calibration
import commun

NL = chr(10)
PRM = commun.charger_parametres(environ={})
EP = commun.lire_entree(PRM, "episodes", environ={}).decode("utf-8")
UNITES = commun.lire_entree(PRM, "fiv_unites", environ={}, sommes="sommes_plan2").decode("utf-8")
PRES = calib_fiv.calendrier_e1(PRM, environ={})["presentes"]
EPI = calibration.analyser(EP, PRM["calibration"])["episodes"]
K2 = dict(PRM["calibration"], strates=["calme"], unites=[["binance", "binance"], ["bitfinex", "bitfinex"]], ell=[1, 2])


def ligne_u(st, f, h, ell):
    """Première ligne de fiv_unites.txt versé (section [FIV_u(ℓ)]) de (strate, flux, hôte, ℓ)."""
    return next(x for x in UNITES.split(NL) if x.startswith(f"  « {st} » {f} (hôte {h}) ℓ = {ell} : "))


def indefinie(ell, k="0", fiv="-", n="24585"):
    """Ligne de bitfinex en calme à K = 0 (forme de r1 de f35a70c : σ̂²_bloc et γ̂₀ « 0 », FIV « - ») ; cv et
    garde de la ligne versée de binance au même ℓ (même n)."""
    cv = ligne_u("calme", "binance", "binance", ell).split("cv théorique = ")[1]
    return (f"  « calme » bitfinex (hôte bitfinex) ℓ = {ell} : n = {n} ; K = {k} ; FIV_série = {fiv} ; σ̂²_bloc = 0 ; "
            f"γ̂₀ = 0 ; cv théorique = {cv}")


def unites_fictif(*lignes, controle="aux 2 ℓ", suite="[SENSIBILITÉ VOISINAGE] hors C1") -> str:
    """fiv_unites.txt réduit à K2 (calme ; binance, bitfinex ; ℓ 1 et 2), en-têtes recopiés du fichier versé."""
    return NL.join(["préparation de S2-bis ; ne change pas le verdict de S2 (« R1 discrimine » = FAUX)", "en-tête",
                    "[FIV_u(ℓ)] série d'écart de l'hôte u (r1.ECARTS) sur les fenêtres retenues de la strate, "
                    "pool D1-bis ; FIV_série = σ̂²_bloc/γ̂₀ de r1.block_long_run_variance (forme d'EP l.94) ; garde "
                    "n ≥ 30·ℓ imprimée", "  contrôle : n et K de chaque hôte = n_s et cellules « ecart » d'EP ; "
                    f"FIV_série de I_t (D1-bis) recalculée depuis les D_u = EP {controle} : égaux", *lignes, suite, ""])


def retouche(numero: int, avant: str, apres: str) -> str:
    """EP avec, à la ligne `numero` (1 = première), l'unique occurrence de `avant` remplacée par `apres`."""
    lignes = EP.split(NL)
    assert lignes[numero - 1].count(avant) == 1, (numero, avant)
    lignes[numero - 1] = lignes[numero - 1].replace(avant, apres)
    return NL.join(lignes)


class TestCalibration(unittest.TestCase):
    def refus(self, code, texte, k=None):
        """Refus nommé `code` exigé ; toute autre exception échoue en la nommant par son type (O-1, R-12 de la G2)."""
        try:
            calibration.analyser(texte, k or PRM["calibration"])
        except Exception as e:
            self.assertEqual(getattr(e, "code", type(e).__name__), code)
        else:
            self.fail(f"{code} attendu, aucun refus")

    def test_lecture_t_cal_1(self):
        """EP l.13 et l.14 ; 40 lignes d'épisodes (2 strates × 10 unités × 2 types). Mutations M-CAL-1 (censurés
        ajoutés aux complets), M-2-03 (nombre décimal lu en flottant)."""
        c = calibration.charger(PRM, environ={})
        self.assertEqual(c["episodes"]["calme", "binance", "panne"], {
            "n_s": 24585, "cellules": 372, "episodes": 332, "censures": 51, "complets": 281, "max": 5,
            "taux": Fraction("0.015131177547284929835265405735204392922513727882855"),
            "moyenne": Fraction("1.1204819277108433734939759036144578313253012048193"), "quantiles": [1, 1, 3],
            "moyenne_complets": Fraction("1.1209964412811387900355871886120996441281138790036"),
            "histogramme": [(1, 301), (2, 24), (3, 6), (5, 1)]})
        self.assertEqual(len(c["episodes"]), 40)

    def test_parametres_et_epingles(self):
        """Section « calibration » ; EP sous une épingle fausse : refus du socle. Mutation M-2-04 : EP lu sans
        commun.lire_entree."""
        k = PRM["calibration"]
        self.assertEqual((k["strates"], k["types"], k["pools"], k["quantiles"], k["garde_blocs"], k["precision"]),
                         (["calme", "stress"], ["panne", "ecart"], ["S2 (D1)", "D1-bis"], [50, 90, 99], 30, 50))
        self.assertEqual([h for h, _f in k["unites"]], ["binance", "bitfinex", "bitstamp", "chainlink", "coinbase",
                                                        "coingecko", "defillama", "gemini", "kraken", "okx"])
        faux = dict(PRM, entrees=dict(PRM["entrees"], episodes=dict(PRM["entrees"]["episodes"], sha256="0" * 64)))
        with self.assertRaises(commun.Refus) as c:
            calibration.charger(faux, environ={})
        self.assertEqual(c.exception.code, "ENTREE/sha256-parametres")

    def test_refus_de_forme(self):
        """Première ligne, type hors d'ordre, exposant, ligne d'histogramme ôtée, ligne en trop, saut final ôté, valeur
        « - », virgule décimale : CALIB/forme. Mutations M-2-05 (nombre de lignes non contrôlé), M-2-06 (identité de
        ligne non contrôlée), M-2-07 (première ligne non contrôlée)."""
        h14 = "    histogramme (longueur×nombre) : 1×301 2×24 3×6 5×1" + NL
        for t in (retouche(1, "S2-bis", "S2bis"), retouche(17, ") panne", ") ecart"),
                  retouche(13, "P99 = 3", "P99 = 3E0"), EP.replace(h14, "", 1), EP + "x" + NL, EP[:-1],
                  retouche(25, "moyenne = 1.15 ;", "moyenne = - ;"), retouche(65, "taux = 0.0", "taux = 0,0")):
            self.refus("CALIB/forme", t)

    def test_refus_de_coherence(self):
        """Une retouche par contrôle, qui ne rougit que lui : taux ≠ cellules/n_s (E-S-37), moyenne, complets ≠
        épisodes − censurés, maximum, somme des nombres, somme des longueurs, ordre des longueurs, quantile, n_s = 0
        (quotient impossible) : CALIB/coherence. Mutations M-2-08 à M-2-16, un contrôle retiré chacune ; M-2-33
        (nombre nul admis)."""
        for t in (retouche(13, "727882855 ;", "727882856 ;"), retouche(13, "2048193 ;", "2048194 ;"),
                  retouche(13, "censurés 51", "censurés 52"), retouche(13, "max = 5", "max = 6"),
                  retouche(14, "1×301 2×24", "1×303 2×23"), retouche(14, "1×301 2×24", "1×302 2×23"),
                  retouche(14, "3×6 5×1", "5×1 3×6"), retouche(14, "3×6 5×1", "3×6 4×0 5×1"),
                  retouche(13, "P99 = 3", "P99 = 2"),
                  retouche(13, "n_s = 24585 ;", "n_s = 0 ;")):
            self.refus("CALIB/coherence", t)

    def test_lecture_fiv_t_cal_1(self):
        """EP l.140 (D1-bis, calme, ℓ = 240, garde tenue) et l.144 (ℓ = 1440, garde non tenue) ; 4 courbes de 17 points.
        Mutation M-CAL-2 : garde ignorée (lue tenue partout)."""
        d = calibration.charger(PRM, environ={})["fiv"]
        self.assertEqual(d["D1-bis", "calme"][12], {
            "ell": 240, "n": 24585, "K": 148, "fiv": Fraction("22.875107619499139688158815002722346438402490494255"),
            "sigma2": Fraction("3365.1353559023660984670112023097760840941942530323"),
            "gamma0": Fraction("147.10905023388244864754931869025828757372381533455"),
            "cv": Fraction("0.11408797792643129814123654880491384644099142081780"), "garde": True})
        self.assertEqual((d["D1-bis", "calme"][16]["ell"], d["D1-bis", "calme"][16]["garde"]), (1440, False))
        self.assertEqual([(cle, len(v)) for cle, v in d.items()],
                         [(("S2 (D1)", "calme"), 17), (("S2 (D1)", "stress"), 17), (("D1-bis", "calme"), 17),
                          (("D1-bis", "stress"), 17)])

    def test_refus_fiv(self):
        """ℓ hors grille : CALIB/forme ; FIV ≠ σ̂²/γ̂₀, γ̂₀ ≠ (nK − K²)/n (σ̂² et γ̂₀ retouchés ensemble à ℓ = 1,
        FIV = 1 tenu), garde ≠ (n ≥ 30ℓ), cv ≠ √(4ℓ/3n) : CALIB/coherence. Mutations M-2-17 à M-2-20, un contrôle
        retiré chacune."""
        self.refus("CALIB/forme", retouche(161, "ℓ = 1440", "ℓ = 1441"))
        g = "147.10905023388244864754931869025828757372381533455"
        for t in (retouche(140, "494255 ;", "494256 ;"),
                  retouche(128, f"σ̂²_bloc = {g} ; γ̂₀ = {g}", "σ̂²_bloc = 2 ; γ̂₀ = 2"),
                  retouche(140, "garde : tenue", "garde : non tenue"), retouche(140, "4099142081780", "4099142081781")):
            self.refus("CALIB/coherence", t)

    def test_quotient_indefini_nomme(self):
        """C-5 de la G2 (R-12) : EP l.13 « n_s = 0 ; cellules = 0 » : 0/0 lève InvalidOperation, qui n'est pas une
        ZeroDivisionError ; rendu CALIB/coherence. Mutation R-12 : seules les divisions par zéro nommées."""
        self.refus("CALIB/coherence", retouche(13, "n_s = 24585 ; cellules = 372 ;", "n_s = 0 ; cellules = 0 ;"))

    def test_longueur_repetee_refusee(self):
        """C-5 de la G2 (R-13) : EP l.14 « 1×301 » écrit « 1×300 1×1 » (332 épisodes, 372 cellules, maximum et
        quantiles inchangés, `bc`) : longueurs non strictement croissantes, CALIB/coherence. Mutation R-13 :
        « sorted(lg) » au lieu de « sorted(set(lg)) »."""
        self.refus("CALIB/coherence", retouche(14, "1×301", "1×300 1×1"))

    def test_lecture_fiv_unites(self):
        """Point (1) de l'ajout daté du G0 du 2026-10-05 15:05:43 UTC : fiv_unites.txt versé, sous ses deux épingles
        (sommes de PLAN-S2BIS-2) ; 2 strates × 10 hôtes du format × 17 ℓ ; l.28 (calme, binance, ℓ = 240, garde
        tenue) recopiée ; ℓ = 1 440 non gardé en calme, ℓ = 360 gardé et 480 non gardé en stress (n = 11 397, okx :
        K = 6) ; sensibilité au voisinage non lue (l.371 : n = 24 081). Mutations M-15D-01 (lu sous les sommes de
        PLAN-S2BIS), M-15D-02 (flux et hôte permutés dans le préfixe)."""
        lus = {}
        d = calibration.charger_unites(PRM, PRES, EPI, lus, environ={})
        self.assertEqual(sorted(lus), ["docs/adr-0029/plan-s2bis-2/SHA256SUMS",
                                       "docs/adr-0029/plan-s2bis-2/fiv_unites.txt"])
        self.assertEqual([(s, list(v), {len(x) for x in v.values()}) for s, v in d.items()],
                         [(s, [h for h, _f in PRM["calibration"]["unites"]], {17}) for s in ("calme", "stress")])
        self.assertEqual(d["calme"]["binance"][12], {
            "ell": 240, "n": 24585, "K": 372, "fiv": Fraction("15.597399630566863574612592724178660092896456256288"),
            "sigma2": Fraction("5714.4380499828575959462774553003903852145741331732"),
            "gamma0": Fraction("366.37120195241000610128126906650396583282489322758"),
            "cv": Fraction("0.11408797792643129814123654880491384644099142081780"), "garde": True})
        o = d["stress"]["okx"]
        self.assertEqual((d["calme"]["binance"][16]["garde"], o[13]["ell"], o[13]["garde"], o[14]["garde"], o[13]["n"],
                          o[13]["K"]), (False, 360, True, False, 11397, 6))

    def test_fiv_unites_indefini(self):
        """Fixture réduite : bitfinex à K = 0 (FIV « - », σ̂²_bloc et γ̂₀ « 0 ») lu indéfini (None), binance recopié ;
        EP l.140 à FIV « - » : CALIB/forme (EP n'admet pas l'indéfini) ; K = 3 avec γ̂₀ écrit « 0 » (refusé par le
        contrôle de γ̂₀), FIV « 1 » à K = 0, n = 0 (quotient impossible), n différent entre hôtes de la strate (lignes
        de stress recopiées sous « calme ») : CALIB/coherence ; CC-2 du contre-contrôle : ligne de binance à ℓ = 1
        (n = 24 585, K = 372, γ̂₀ et cv recopiés, cohérents) réécrite FIV « - » et σ̂²_bloc = 0 : CALIB/coherence par
        la seule règle « - » si et seulement si γ̂₀ = 0 ; hôtes permutés, section suivante absente, contrôle à 17 ℓ,
        étiquette retouchée, texte arrêté après l'en-tête de la section : CALIB/forme. Mutations M-15D-03 (« - »
        refusé partout), M-15D-04 (« - » admis dans EP), M-15D-05 (n commun non contrôlé), M-15D-06 (section
        suivante non contrôlée), MR-18 du réviseur (« - » décidé sur σ̂²_bloc)."""
        b1, b2 = ligne_u("calme", "binance", "binance", 1), ligne_u("calme", "binance", "binance", 2)
        g0 = b1.split("γ̂₀ = ")[1].split(" ;")[0]
        b0 = b1.replace(f"FIV_série = 1 ; σ̂²_bloc = {g0} ;", "FIV_série = - ; σ̂²_bloc = 0 ;")
        self.assertEqual((b0 != b1, " : n = 24585 ; K = 372 ; FIV_série = - ; σ̂²_bloc = 0 ; γ̂₀ = " + g0 in b0),
                         (True, True))
        d = calibration.analyser_unites(unites_fictif(b1, b2, indefinie(1), indefinie(2)), K2)
        self.assertEqual([[x["fiv"] for x in v] for v in d["calme"].values()],
                         [[1, Fraction(b2.split("FIV_série = ")[1].split(" ;")[0])], [None, None]])
        self.refus("CALIB/forme", retouche(140, "FIV_série = 22.875107619499139688158815002722346438402490494255",
                                           "FIV_série = -"))
        s1, s2 = (ligne_u("stress", "bitfinex", "bitfinex", e).replace("« stress »", "« calme »") for e in (1, 2))
        for code, texte in (("CALIB/coherence", unites_fictif(b1, b2, indefinie(1, k="3"), indefinie(2))),
                            ("CALIB/coherence", unites_fictif(b1, b2, indefinie(1, fiv="1"), indefinie(2))),
                            ("CALIB/coherence", unites_fictif(b1, b2, indefinie(1, n="0"), indefinie(2))),
                            ("CALIB/coherence", unites_fictif(b1, b2, s1, s2)),
                            ("CALIB/coherence", unites_fictif(b0, b2, indefinie(1), indefinie(2))),
                            ("CALIB/forme", unites_fictif(indefinie(1), indefinie(2), b1, b2)),
                            ("CALIB/forme", unites_fictif(b1, b2, indefinie(1), indefinie(2), suite="fin")),
                            ("CALIB/forme", unites_fictif(b1, b2, indefinie(1), indefinie(2), controle="aux 17 ℓ")),
                            ("CALIB/forme", unites_fictif(b1, b2, indefinie(1), indefinie(2)).replace("FAUX", "VRAI")),
                            ("CALIB/forme", NL.join(unites_fictif(b1).split(NL)[:3]))):
            with self.assertRaises(commun.Refus) as c:
                calibration.analyser_unites(texte, K2)
            self.assertEqual(c.exception.code, code, texte.split(NL)[4:8])

    def test_croisement_q_si_9(self):
        """Q-SI-9 (adjugée le 2026-10-08, fermée dans ce lot) : par strate et par hôte, chaque ligne de fiv_unites.txt
        a n = positions présentes du masque d'E1, n = n_s et K = cellules « ecart » d'EP ; données versées : égaux
        (mesuré hors code : 20 couples, calme 24 585, stress 11 397). Retouches, chacune sur le dernier hôte du format
        (okx) ou la dernière ligne seulement : masque de calme amputé d'une position, cellules ou n_s d'EP, K ou n de
        la ligne ℓ = 1 440 ; strate absente du masque, hôte absent d'EP : CALIB/croisement, jamais KeyError ni
        AttributeError ; charger_unites fait le contrôle, et un appel sans presentes ni ep lève TypeError (CC-1 du
        contre-contrôle). Mutations M-15G-01 à M-15G-12, MG-14 du réviseur (presentes et ep facultatifs)."""
        u, cle = calibration.analyser_unites(UNITES, PRM["calibration"]), ("stress", "okx", "ecart")
        self.assertIsNone(calibration.croiser_unites(u, PRES, EPI))
        self.assertEqual({x["n"] for v in u.values() for xs in v.values() for x in xs}, {24585, 11397})
        e, d = EPI[cle], dict(EPI)
        del d[cle]
        coupe = dict(PRES, calme=PRES["calme"] & (PRES["calme"] - 1))

        def ligne(**k):
            v = {s: {h: list(xs) for h, xs in hs.items()} for s, hs in u.items()}
            v["stress"]["okx"][-1] = dict(v["stress"]["okx"][-1], **k)
            return v
        ok, x = u, u["stress"]["okx"][-1]
        cas = [(ok, coupe, EPI), (ok, PRES, {**EPI, cle: dict(e, cellules=e["cellules"] + 1)}),
               (ok, PRES, {**EPI, cle: dict(e, n_s=e["n_s"] + 1)}), (ligne(K=x["K"] + 1), PRES, EPI),
               (ligne(n=x["n"] + 1), PRES, EPI), (ok, {"calme": PRES["calme"]}, EPI), (ok, PRES, d)]
        for v, p, ep in cas:
            with self.assertRaises(commun.Refus) as c:
                calibration.croiser_unites(v, p, ep)
            self.assertEqual(c.exception.code, "CALIB/croisement")
        with self.assertRaises(commun.Refus) as c:
            calibration.charger_unites(PRM, coupe, EPI, environ={})
        self.assertEqual(c.exception.code, "CALIB/croisement")
        with self.assertRaises(TypeError):
            calibration.charger_unites(PRM, environ={})

    def test_quantile_au_dela_de_100(self):
        """O-1 de la G2 : un quantile au-delà de 100 n'a pas de rang (P101 : rang 336 > 332 épisodes, `bc`) : refus
        nommé CALIB/coherence, et non StopIteration. Mutation : next sans valeur par défaut."""
        k = dict(PRM["calibration"], quantiles=[50, 90, 101])
        self.refus("CALIB/coherence", EP.replace("P99 = ", "P101 = "), k)
