"""Sources SB-3 et SB-4 (E-S-07 à E-S-16, E-S-39, E-S-41, E-S-43 ; T-GEN-1, T-GEN-2) : chaîne à deux états de taux
stationnaire b/(1 − a + b) écrit à la main, moyenne simulée à 5 erreurs-types ; renouvellement alterné et incidents
tirés pas à pas par des u écrits à la main ; poids et paramètres refaits à la main en rationnels. Chaque test nomme les
mutations qui le rougissent. Les comparaisons « à 5 SE » se font en rationnels exacts, sans racine :
(x̄ − r)² < 25·s²/R."""
import unittest
from fractions import Fraction

import aleas
import calendrier
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


def fond(f="1", regime=None, longues="0", autres="1", hors="0") -> dict:
    """Fond d'essai : f, régime (φ, κ, τ_D) ou None dans les deux strates, part des pannes longues, multiplicateur
    d'écart des classes autres que BTC, taux hors-enveloppe τ."""
    return {"f": Fraction(f), "regime": {"calme": regime, "stress": regime}, "longues": Fraction(longues),
            "autres": Fraction(autres), "hors_enveloppe": Fraction(hors)}


def part(m: int, debut: int, n: int) -> Fraction:
    """Part des bits à 1 de m dans les fenêtres [debut, debut + n)."""
    return Fraction((m >> debut & ((1 << n) - 1)).bit_count(), n)


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


class TestHotes(unittest.TestCase):
    def test_indice_et_longues(self):
        """Indice (h·S + s)·10 + k, h rang dans sources.indices_hotes (C-6) : binance calme → 0 ; okx (rang 3) stress,
        k = 3 → (3·2 + 1)·10 + 3 = 73 ; bitfinex (rang 6) stress → 130 ; hôte inconnu, k = 10 : SOURCES/indice. Pannes
        longues (E-S-11) : 1 h, 1 jour, 3 jours, également probables, moyenne (60 + 1 440 + 4 320)/3 = 1 940. Mutations
        M-3C-01 (strate omise de l'indice), M-3C-09 (durées pondérées par leur longueur), M-C6-06 (rang pris dans la
        liste triée)."""
        self.assertEqual([sources.indice(PRM, "binance", "calme"), sources.indice(PRM, "okx", "stress", 3),
                          sources.indice(PRM, "bitfinex", "stress")], [0, 73, 130])
        for h, k in (("bybit", 0), ("okx", 10)):
            with self.assertRaises(commun.Refus) as c:
                sources.indice(PRM, h, "calme", k)
            self.assertEqual(c.exception.code, "SOURCES/indice")
        self.assertEqual(PRM["sources"]["longues"], [60, 1440, 4320])
        lg = sources.loi_longues(PRM)
        self.assertEqual((lg.hist, lg.moyenne), (((60, 1), (1440, 1), (4320, 1)), 1940))

    def test_indices_hotes_stables(self):
        """C-6 (avis Q-T2-11) : h pris dans sources.indices_hotes, liste scellée des 10 hôtes D1-bis dans
        l'ordre où l'ADR-0029 l.168 les écrit (recopié ici à la main ; EP l.8 : aucun retrait), distincte de
        calibration.unites (ordre alphabétique). Pool réordonné (à rebours) ou réduit (sans coinbase) : état vrai des
        autres hôtes inchangé à l'octet, rang 1 de coinbase inemployé ; unité faible : indice = rang de l'hôte (kraken :
        2), quelle que soit sa place dans spec["hotes"]. Mutations M-C6-01 (h pris dans calibration.unites), M-C6-02
        (unité faible indexée par sa place dans la spécification), M-C6-04 (liste dans l'ordre alphabétique)."""
        ordre = ["binance", "coinbase", "kraken", "okx", "bitstamp", "gemini", "bitfinex", "coingecko", "defillama",
                 "chainlink"]
        self.assertEqual(PRM["sources"]["indices_hotes"], ordre)
        self.assertEqual(sorted(ordre), [h for h, _f in PRM["calibration"]["unites"]])
        m = {"calme": (1 << 500) - 1, "stress": 0}

        def etat(unites):
            hotes = [h for h, _f in unites]
            cl = {c: [h for h in hotes if h in p] for c, p in PRM["sources"]["classes"].items()}
            prm = dict(PRM, calibration=dict(PRM["calibration"], unites=unites),
                       sources=dict(PRM["sources"], classes=cl))
            return sources.Replication(prm, EP, fond(hors="1/50"), "T-C6", 0, m, 500).etat(), prm
        e = etat(PRM["calibration"]["unites"])[0]
        self.assertEqual(etat(list(reversed(PRM["calibration"]["unites"])))[0], e)
        e_red, prm = etat([u for u in PRM["calibration"]["unites"] if u[0] != "coinbase"])
        self.assertEqual(e_red, {k: v for k, v in e.items() if k[0] != "coinbase"})
        self.assertEqual(sorted(sources.indice(prm, h, "calme") // 20 for h, _f in prm["calibration"]["unites"]),
                         [0, 2, 3, 4, 5, 6, 7, 8, 9])
        a_, b = sources.chaine(Fraction(1, 2), 1)
        k = sources.masque(sources.markov(aleas.flux(A, "T-C6", 0, "faibles", 2), a_, b, A, 500))
        for hotes in (["kraken"], ["gemini", "kraken"], ["kraken", "gemini"]):
            spec = {"hotes": hotes, "p": Fraction(1, 2), "L": 1, "type": "panne"}
            self.assertEqual(sources.faibles(PRM, "T-C6", 0, spec, 500)["kraken"], k, hotes)

    def test_indices_hotes_refus(self):
        """C-6 : hôte d'un pool absent de sources.indices_hotes (okx retiré de la liste), par indice(), etat() et
        faibles(), ou liste à doublon : SOURCES/indice. Mutations M-C6-03 (contrôle d'appartenance retiré), M-C6-05
        (contrôle des doublons retiré)."""
        ordre, m = PRM["sources"]["indices_hotes"], {"calme": (1 << 500) - 1, "stress": 0}
        sans_okx = dict(PRM, sources=dict(PRM["sources"], indices_hotes=[h for h in ordre if h != "okx"]))
        double = dict(PRM, sources=dict(PRM["sources"], indices_hotes=ordre + ["binance"]))
        spec = {"hotes": ["okx"], "p": Fraction(1, 2), "L": 1, "type": "panne"}
        for prm, appel in ((sans_okx, lambda p: sources.indice(p, "okx", "calme")),
                           (sans_okx, lambda p: sources.Replication(p, EP, fond(), "T-C6", 0, m, 500).etat()),
                           (sans_okx, lambda p: sources.faibles(p, "T-C6", 0, spec, 500)),
                           (double, lambda p: sources.indice(p, "kraken", "calme"))):
            with self.assertRaises(commun.Refus) as c:
                appel(prm)
            self.assertEqual(c.exception.code, "SOURCES/indice")

    def test_regime_part_phi(self):
        """Régime Z (E-S-12) : durée moyenne τ_D = 20 en régime dégradé, part φ = 1/5, d'où a = 19/20 et
        b = φ/(τ_D(1 − φ)) = 1/80 ; 300 réplications de 2 000 fenêtres : part de Z à moins de 5 SE de 1/5 ; C0 : Z = 0.
        φ = 1, κ < 1 ou τ_D = 0 : SOURCES/regime. Mutation M-3C-02 : b = φ/τ_D (part φ/(1 + φ) = 1/6)."""
        m = {"calme": (1 << 2000) - 1, "stress": 0}
        x = [part(sources.Replication(PRM, EP, fond(regime=(Fraction(1, 5), Fraction(3), 20)), "T-Z", i, m, 2000)
                  .regime("binance", "calme"), 0, 2000) for i in range(300)]
        self.assertTrue(dans_5_se(x, Fraction(1, 5)))
        self.assertEqual(sources.Replication(PRM, EP, fond(), "T-Z", 0, m, 2000).regime("binance", "calme"), 0)
        for reg in ((Fraction(1), Fraction(3), 20), (Fraction(1, 5), Fraction(1, 2), 20),
                    (Fraction(1, 5), Fraction(3), 0)):
            with self.assertRaises(commun.Refus) as c:
                sources.Replication(PRM, EP, fond(regime=reg), "T-Z", 0, m, 2000).regime("binance", "calme")
            self.assertEqual(c.exception.code, "SOURCES/regime")

    def test_regime_garde_avant_usage(self):
        """C-2 de la G2 de la tranche 2 (E-S-12) : régime invalide refusé SOURCES/regime par le chemin principal, avant
        tout usage dans union(), par pannes() comme par etat() : κ = 1/2 (auparavant ALEAS/geometrique) ; à κ = 1
        (r' = 0, Z jamais tiré), φ = 2 ou τ_D = 0 (auparavant admis en silence). Mutation M-C2-01 : contrôle retiré
        d'union()."""
        m = {"calme": (1 << 500) - 1, "stress": 0}
        for reg in ((Fraction(1, 5), Fraction(1, 2), 20), (Fraction(2), Fraction(1), 20),
                    (Fraction(1, 5), Fraction(1), 0)):
            for chemin in ("pannes", "etat"):
                r = sources.Replication(PRM, EP, fond(regime=reg), "T-C2", 0, m, 500)
                with self.assertRaises(commun.Refus) as c:
                    r.pannes("binance") if chemin == "pannes" else r.etat()
                self.assertEqual(c.exception.code, "SOURCES/regime", (reg, chemin))

    def test_union_taux_marginal(self):
        """Taux marginal conservé (E-S-11, E-S-12) : p = 1/10, loi 1×1 3×1, part longue 1/2 (durées 2 et 4 dans un
        paramètre d'essai), régime φ = 1/5, κ = 10, τ_D = 20 ; 300 réplications de 2 000 fenêtres : part du temps dans E
        ∪ (E′ ∩ Z) ∪ L à moins de 5 SE de 1/10. Point de la grille E1 à f = 1 (defillama stress, p = 226/11 397, EP
        l.77 ; φ = 1/100, κ = 50 ; loi regroupée, μ = 684/673) : r' = r_E·49/(1 − r_E), r_E = 100p/149, soit
        1 107 400/1 675 553 ≈ 0,66, au-delà de μ/(μ + 1) = 684/1 357 : admis, E′ étant tirée indépendamment ; p = 1/10
        donne r' > 1 : SOURCES/taux. Mutations M-3C-03 (E′ hors de Z), M-3C-04 (pannes longues omises), M-3C-15 (E′ en
        épisodes de la loi d'EP), M-3C-16 (contrôle r' < 1 retiré)."""
        prm = dict(PRM, sources=dict(PRM["sources"], longues=[2, 4]))
        loi, m = sources.Empirique([(1, 1), (3, 1)]), {"calme": (1 << 2000) - 1, "stress": 0}
        x = []
        for i in range(300):
            r = sources.Replication(prm, EP, fond(longues="1/2", regime=(Fraction(1, 5), Fraction(10), 20)), "T-U", i,
                                    m, 2000)
            x.append(part(r.union("binance", "calme", 0, Fraction(1, 10), loi, ("panne", "panne-regime", "longues")),
                          0, 2000))
        self.assertTrue(dans_5_se(x, Fraction(1, 10)))
        r = sources.Replication(PRM, EP, fond(regime=(Fraction(1, 100), Fraction(50), 60)), "T-U", 0, m, 6000)
        loi = sources.loi_longueurs(PRM, EP, "stress", "defillama", "panne")
        noms = ("panne", "panne-regime", None)
        self.assertNotEqual(r.union("defillama", "stress", 0, Fraction(226, 11397), loi, noms), 0)
        with self.assertRaises(commun.Refus) as c:
            r.union("defillama", "stress", 0, Fraction(1, 10), loi, noms)
        self.assertEqual(c.exception.code, "SOURCES/taux")

    def test_pannes_par_strate(self):
        """H(hôte) (E-S-08, E-S-09) : coingecko, f = 1/2, sans régime ni panne longue ; grille de 2 × 10 080 fenêtres,
        calme la première moitié, stress la seconde ; 100 réplications : part en panne de chaque moitié à moins de 5 SE
        de f·56/24 585 (EP l.33) et de f·127/11 397 (EP l.73) ; strates vides : aucune panne. Mutations M-3C-05 (masque
        de strate non appliqué), M-3C-06 (écart propre au lieu de la panne), M-3C-07 (f ignoré), M-3C-08 (taux du calme
        dans les deux strates)."""
        n = 10080
        m = {"calme": (1 << n) - 1, "stress": ((1 << n) - 1) << n}
        h = [sources.Replication(PRM, EP, fond("1/2"), "T-H", i, m, 2 * n).pannes("coingecko") for i in range(100)]
        self.assertTrue(dans_5_se([part(x, 0, n) for x in h], Fraction(28, 24585)))
        self.assertTrue(dans_5_se([part(x, n, n) for x in h], Fraction(127, 22794)))
        vide = {"calme": 0, "stress": 0}
        self.assertEqual(sources.Replication(PRM, EP, fond(), "T-H", 0, vide, n).pannes("kraken"), 0)


class TestDerives(unittest.TestCase):
    def refus(self, code, f, *a):
        with self.assertRaises(commun.Refus) as c:
            f(*a)
        self.assertEqual(c.exception.code, code)

    def test_parametres_et_multiplicateur(self):
        """E-S-13 : bornes 0,1 et 1,9, trois unités à saut, transitoire × 3 la première semaine (10 080 fenêtres), panne
        initiale de 3 jours (4 320). m(t) linéaire de 1/10 à 19/10 sur L = 100 : 1/10, 1 (t = 50), 19/10, puis tenu
        (t = 150) ; saut de 19/10 à 1/10 en 30 : 19/10 à t = 29, 1/10 à t = 30. Mutations M-3D-01 (t non borné par L),
        M-3D-02 (saut en t ≤ x)."""
        self.assertEqual(PRM["sources"]["derive"], {"bornes": [[1, 10], [19, 10]], "unites_saut": 3,
                                                    "transitoire": [3, 10080], "initiale": 4320})
        d = ("lineaire", Fraction(1, 10), Fraction(19, 10), 100)
        self.assertEqual([sources.multiplicateur(d, t) for t in (0, 50, 100, 150)],
                         [Fraction(1, 10), 1, Fraction(19, 10), Fraction(19, 10)])
        s = ("saut", Fraction(19, 10), Fraction(1, 10), 30)
        self.assertEqual([sources.multiplicateur(s, t) for t in (29, 30)], [Fraction(19, 10), Fraction(1, 10)])

    def test_amincir(self):
        """Épisode gardé si u < m(début)/M : saut de 3 à 1 en 10 (M = 3) : débuts 0 et 5 gardés même à u = 0,9
        (m/M = 1) ; débuts 12 et 20 à 1/3 : u = 0,3 garde, 0,4 retire. Linéaire de 1/10 à 19/10 sur 100 : m(0)/M = 1/19,
        u = 0,06 retire ; m(50)/M = 10/19, u = 0,5 garde. Mutation M-3D-03 : M = m0 au lieu de max(m0, m1)."""
        segs = [(0, 2), (5, 6), (12, 15), (20, 21)]
        self.assertEqual(sources.amincir(suite(0.9, 0.9, 0.3, 0.4), segs, ("saut", Fraction(3), Fraction(1), 10)),
                         [(0, 2), (5, 6), (12, 15)])
        d = ("lineaire", Fraction(1, 10), Fraction(19, 10), 100)
        self.assertEqual(sources.amincir(suite(0.06, 0.5), [(0, 3), (50, 51)], d), [(50, 51)])

    def test_derives_tirees(self):
        """Sauts et panne initiale (N9), L = 2 880 (deux jours) : hôte parmi 10 (u = 0,05 → binance), sens (0,7 → de
        19/10 à 1/10), jour (0,6 → 1), minute (0 → 0) : saut en 1 440 ; parmi les 9 restants (0,95 → okx), sens (0,2 →
        de 1/10 à 19/10), jour (0,1 → 0), minute (0,5 → 720) ; parmi 8 (0,3 → chainlink), sens (0,4), jour (0,99 → 1),
        minute (0,99999 → 1 439) : 2 879 ; panne initiale parmi les 9 hôtes décalés (0,05 → rang 0 → bitfinex ; binance,
        non décalé, est exclu). Genre inconnu, deux multiplicateurs, L non multiple d'un jour : SOURCES/derive.
        Mutations M-3D-04 (tirage avec remise), M-3D-05 (hôte non décalé admis pour la panne initiale), M-3D-06
        (contrôle des genres retiré)."""
        u = suite(0.05, 0.7, 0.6, 0.0, 0.95, 0.2, 0.1, 0.5, 0.3, 0.4, 0.99, 0.99999, 0.05)
        lo, hi = Fraction(1, 10), Fraction(19, 10)
        self.assertEqual(sources.derives(PRM, {"genres": ["sauts", "initiale"], "duree": 2880}, u),
                         {"specs": {"binance": ("saut", hi, lo, 1440), "okx": ("saut", lo, hi, 720),
                                    "chainlink": ("saut", lo, hi, 2879)}, "initiale": "bitfinex"})
        for g, n in ((["inconnu"], 2880), (["tendances", "commune"], 2880), (["sauts"], 1000)):
            self.refus("SOURCES/derive", sources.derives, PRM, {"genres": g, "duree": n}, suite(0.1, 0.1, 0.1, 0.1))

    def test_transitoire_et_initiale(self):
        """Transitoire commun (X2) : binance calme, f = 1, taux × 3 sur les 10 080 premières fenêtres, puis × 1 ; 100
        réplications de 20 160 fenêtres : part en panne à moins de 5 SE de 3·372/24 585 puis de 372/24 585. Panne
        initiale (N9) : l'hôte tiré est en panne sur les 4 320 premières fenêtres. Mutations M-3D-07 (série non tirée au
        taux M·p), M-3D-08 (amincissement omis), M-3D-09 (panne initiale omise)."""
        n, p = 10080, Fraction(372, 24585)
        m = {"calme": (1 << 2 * n) - 1, "stress": 0}
        f = dict(fond(), derive={"genres": ["transitoire"], "duree": n})
        h = [sources.Replication(PRM, EP, f, "T-X2", i, m, 2 * n).pannes("binance") for i in range(100)]
        self.assertTrue(dans_5_se([part(x, 0, n) for x in h], 3 * p))
        self.assertTrue(dans_5_se([part(x, n, n) for x in h], p))
        r = sources.Replication(PRM, EP, dict(fond(), derive={"genres": ["initiale"], "duree": n}), "T-N9", 0, m, 2 * n)
        hote = r.derives()["initiale"]
        self.assertEqual(r.pannes(hote) & ((1 << 4320) - 1), (1 << 4320) - 1)


class TestClasses(unittest.TestCase):
    TOUS = ["binance", "bitfinex", "bitstamp", "chainlink", "coinbase", "coingecko", "defillama", "gemini", "kraken",
            "okx"]

    def test_classes_e_s_07(self):
        """Pools provisoires (E-S-07 ; ADR l.173, P6 C3, CALIB-ACTIFS-G0 §1) : BTC, ETH et USDT servis par les 10 hôtes,
        USDC par 8 (ni coinbase, ni okx) ; pool BTC autre que le pool D1-bis, ou hôte hors du pool : SOURCES/classes.
        Mutation M-4A-01 : contrôle des pools retiré."""
        usdc = [h for h in self.TOUS if h not in ("coinbase", "okx")]
        self.assertEqual(sources.classes(PRM), [("BTC", self.TOUS), ("ETH", self.TOUS), ("USDC", usdc),
                                                ("USDT", self.TOUS)])
        for c, pool in (("BTC", self.TOUS[1:]), ("ETH", self.TOUS + ["bybit"])):
            prm = dict(PRM, sources=dict(PRM["sources"], classes=dict(PRM["sources"]["classes"], **{c: pool})))
            with self.assertRaises(commun.Refus) as e:
                sources.classes(prm)
            self.assertEqual(e.exception.code, "SOURCES/classes")

    def test_jointe_t_gen_2(self):
        """T-GEN-2 : fond nul (f = 0, τ = 0), panne d'hôte écrite à la main sur kraken (fenêtres 3, 4, 5) : elle frappe
        les 4 classes de kraken, typée panne, et aucune autre des 38 séries (10 + 10 + 8 + 10). Fond f = 1, τ = 1/10 :
        la panne de binance (372/24 585 en calme, EP l.13) est la même dans ses 4 classes et non vide, ses écarts
        diffèrent d'une classe à l'autre, et aucun écart ne recouvre une panne. Mutations M-GEN-3 (H tirée par classe),
        M-4A-02 (surcharge sur la seule première classe), M-4A-03 (écart non disjoint de la panne)."""
        m, n = {"calme": (1 << 2000) - 1, "stress": 0}, 2000
        e = sources.Replication(PRM, EP, fond("0"), "T-GEN-2", 0, m, n).etat({"kraken": 0b111000})
        self.assertEqual(len(e), 38)
        self.assertEqual({k: v for k, v in e.items() if v != (0, 0)},
                         {("kraken", c): (0b111000, 0) for c in ("BTC", "ETH", "USDC", "USDT")})
        e = sources.Replication(PRM, EP, fond("1", hors="1/10"), "T-GEN-2", 0, m, n).etat()
        pannes = {e["binance", c][0] for c in ("BTC", "ETH", "USDC", "USDT")}
        ecarts = [e["binance", c][1] for c in ("BTC", "ETH", "USDC", "USDT")]
        self.assertEqual((len(pannes), len(set(ecarts)), any(x & y for x, y in e.values())), (1, 4, False))
        self.assertNotEqual(pannes, {0})

    def test_ecarts_e_s_09(self):
        """F (E-S-09, Q-S-21) sur un EP d'essai où binance calme compte 2 830 cellules d'écart pour 372 de panne (écart
        propre 2 458/24 585) : f = 1/2, autres = 2, τ = 1/20 ; 100 réplications de 10 080 fenêtres : part de F à moins
        de 5 SE de 1 − (1 − 1 229/24 585)(19/20) pour BTC et de 1 − (1 − 2 458/24 585)(19/20) pour ETH (F d'ETH = F de
        BTC × autres) ; f = 0, τ = 1/10 : épisodes d'une fenêtre seulement, part à moins de 5 SE de 1/10. Mutations
        M-4A-04 (autres non appliqué), M-4A-05 (τ multiplié par f), M-4A-06 (f non appliqué à F), M-4A-07 (taux de panne
        au lieu de l'écart propre), M-4A-08 (épisodes hors-enveloppe de deux fenêtres)."""
        ep = dict(EP)
        ep["calme", "binance", "ecart"] = dict(EP["calme", "binance", "ecart"], cellules=2830)
        n, m, x = 10080, {"calme": (1 << 10080) - 1, "stress": 0}, {0: [], 1: []}
        for i in range(100):
            r = sources.Replication(PRM, ep, fond("1/2", autres="2", hors="1/20"), "T-F", i, m, n)
            for c in (0, 1):
                x[c].append(part(r.ecarts("binance", c), 0, n))
        self.assertTrue(dans_5_se(x[0], 1 - (1 - Fraction(1229, 24585)) * Fraction(19, 20)))
        self.assertTrue(dans_5_se(x[1], 1 - (1 - Fraction(2458, 24585)) * Fraction(19, 20)))
        f = [sources.Replication(PRM, ep, fond("0", hors="1/10"), "T-F", i, m, n).ecarts("kraken", 2)
             for i in range(50)]
        self.assertEqual([y & (y >> 1) for y in f], [0] * 50)
        self.assertTrue(dans_5_se([part(y, 0, n) for y in f], Fraction(1, 10)))


AS = ["bitfinex", "chainlink", "coinbase", "coingecko", "defillama", "kraken", "okx"]


def inc(rho, duree, hotes, geometrique=False) -> dict:
    return {"rho": Fraction(rho), "duree": duree, "geometrique": geometrique, "hotes": hotes}


class TestAlternatives(unittest.TestCase):
    def test_incidents_pas_a_pas(self):
        """E-S-15 : ρ = 720 par jour, soit 720·60/86 400 = 1/2 par fenêtre (pauses géométriques de seuils 1/2, 3/4, 7/8,
        …), horizon 8. D = 2 fixe, paire tirée parmi bitfinex, chainlink, coinbase : début 0 (u = 0,3), paire chainlink
        (v = 0,5, seuils 1/3, 2/3), coinbase (0,9) ; début 3 (0,8), paire bitfinex (0,1), chainlink (0,1) ; pause 5
        au-delà de l'horizon (0,95). D = 3, chacun à 1/2 : début 6 (0,99), coupé à 8, bitfinex et coinbase (v = 0,4,
        0,6, 0,2) ; début 7 (0,3), aucun hôte. D géométrique de moyenne 2 : 0 à 2 (u = 0,3, 0,6), 5 coupé à 8 (pause 5 à
        0,95 ; durée 7 à 0,99), pause 3 au-delà (0,8). Paramètre AS13335 : les 7 hôtes de la partition de S2. Mutations
        M-4B-01 (premier début décalé d'une fenêtre), M-4B-02 (durée non coupée à l'horizon), M-4B-03 (paire tirée avec
        remise), M-4B-04 (w ignoré dans ρ·w)."""
        self.assertEqual(PRM["sources"]["as13335"], AS)
        trois = ["bitfinex", "chainlink", "coinbase"]
        self.assertEqual(sources.incidents(PRM, "T-I", 0, inc(720, 2, ("parmi", trois, 2, [])), 8,
                                           suite(0.3, 0.8, 0.95), suite(0.5, 0.9, 0.1, 0.1)),
                         {"chainlink": 0b11011, "coinbase": 0b11, "bitfinex": 0b11000})
        self.assertEqual(sources.incidents(PRM, "T-I", 0, inc(720, 3, ("chacun", trois, Fraction(1, 2))), 8,
                                           suite(0.99, 0.3), suite(0.4, 0.6, 0.2, 0.9, 0.9, 0.9)),
                         {"bitfinex": 0b11000000, "coinbase": 0b11000000})
        self.assertEqual(sources.incidents(PRM, "T-I", 0, inc(720, 2, ("chacun", ["bitfinex"], Fraction(1)), True), 8,
                                           suite(0.3, 0.6, 0.95, 0.99, 0.8), suite(0.7, 0.1)),
                         {"bitfinex": 0b11100011})

    def test_incidents_hotes_q_s_05(self):
        """D = 1, ρ = 144 par jour (1/10 par fenêtre), 100 réplications de 2 000 fenêtres. Cible, chacun des 7 hôtes
        AS13335 à 7/10 : part de bitfinex à moins de 5 SE de 7/100, de bitfinex et kraken ensemble de 49/1 000. Paire
        tirée par incident : 0 ou 2 hôtes AS13335 par fenêtre, part de bitfinex à moins de 5 SE de (1/10)(2/7). Paire
        imposant okx : okx = bitfinex | chainlink. Hôte hors du pool : SOURCES/incident. Mutations M-4B-05 (un seul
        tirage pour tous les hôtes), M-4B-06 (imposés ignorés), M-4B-07 (contrôle des hôtes retiré)."""
        x, y, z = [], [], []
        for i in range(100):
            e = sources.incidents(PRM, "T-Q", i, inc(144, 1, ("chacun", AS, Fraction(7, 10))), 2000)
            x.append(part(e.get("bitfinex", 0), 0, 2000))
            y.append(part(e.get("bitfinex", 0) & e.get("kraken", 0), 0, 2000))
            e = sources.incidents(PRM, "T-Q", i, inc(144, 1, ("parmi", AS, 2, [])), 2000)
            self.assertEqual({sum(e.get(h, 0) >> t & 1 for h in AS) for t in range(2000)}, {0, 2})
            z.append(part(e.get("bitfinex", 0), 0, 2000))
        self.assertTrue(dans_5_se(x, Fraction(7, 100)))
        self.assertTrue(dans_5_se(y, Fraction(49, 1000)))
        self.assertTrue(dans_5_se(z, Fraction(1, 35)))
        e = sources.incidents(PRM, "T-Q", 0, inc(144, 1, ("parmi", ["bitfinex", "chainlink"], 2, ["okx"])), 2000)
        self.assertEqual(e["okx"], e["bitfinex"] | e["chainlink"])
        with self.assertRaises(commun.Refus) as c:
            sources.incidents(PRM, "T-Q", 0, inc(144, 1, ("chacun", ["bybit"], Fraction(1))), 2000)
        self.assertEqual(c.exception.code, "SOURCES/incident")

    def test_faibles_e_s_16(self):
        """Chaîne (convention de S2, G0 SIM-NIVEAU l.54) : p = 2/5, L = 20 → a = 19/20, b = (2/5)/(20·3/5) = 1/30 ;
        L = 1 : tirages indépendants, a = b = p (p = 3/5, point de bascule, possible). 100 réplications de 1 000
        fenêtres : part à moins de 5 SE de 3/5 (L = 1) et de 2/5 (L = 20). Mutations M-4B-08 (L = 1 en épisodes d'une
        fenêtre, a = 0), M-4B-09 (a et b inversés)."""
        self.assertEqual([sources.chaine(Fraction(2, 5), 20), sources.chaine(Fraction(3, 5), 1)],
                         [(Fraction(19, 20), Fraction(1, 30)), (Fraction(3, 5), Fraction(3, 5))])
        for p, lw in ((Fraction(3, 5), 1), (Fraction(2, 5), 20)):
            x = [part(sources.faibles(PRM, "T-W", i, {"hotes": ["gemini"], "p": p, "L": lw, "type": "panne"},
                                      1000)["gemini"], 0, 1000) for i in range(100)]
            self.assertTrue(dans_5_se(x, p), (p, lw))

    def test_faible_hors_du_pool(self):
        """C-3 de la G2 de la tranche 2 (E-S-16) : unité faible hors du pool (bybit) : SOURCES/faible, par etat()
        (auparavant ignorée en silence) et par faibles(), comme touches() rend SOURCES/incident pour un incident.
        Mutation M-C3-01 : contrôle du pool retiré."""
        spec = {"hotes": ["gemini", "bybit"], "p": Fraction(1, 2), "L": 1, "type": "panne"}
        m = {"calme": (1 << 500) - 1, "stress": 0}
        for appel in (lambda: sources.Replication(PRM, EP, dict(fond("0"), faibles=spec), "T-C3", 0, m, 500).etat(),
                      lambda: sources.faibles(PRM, "T-C3", 0, spec, 500)):
            with self.assertRaises(commun.Refus) as c:
                appel()
            self.assertEqual(c.exception.code, "SOURCES/faible")

    def test_etat_alternatives(self):
        """Fond nul ; incidents sur kraken seul (ρ = 144, D = 2) : la même panne dans les 4 classes de kraken (ADR
        l.162) ; unité faible gemini (p = 1/2, L = 1) de type « ecart » : écart de gemini en BTC seulement ; de type
        « panne » : panne de gemini dans ses 4 classes ; type inconnu : SOURCES/faible. Mutations M-4B-10 (incidents sur
        la seule première classe), M-4B-11 (écart faible dans toutes les classes), M-4B-12 (type non contrôlé)."""
        m, n = {"calme": (1 << 500) - 1, "stress": 0}, 500
        f = dict(fond("0"), incidents=inc(144, 2, ("chacun", ["kraken"], Fraction(1))),
                 faibles={"hotes": ["gemini"], "p": Fraction(1, 2), "L": 1, "type": "ecart"})
        e = sources.Replication(PRM, EP, f, "T-E", 0, m, n).etat()
        k = sources.incidents(PRM, "T-E", 0, f["incidents"], n)["kraken"]
        g = sources.faibles(PRM, "T-E", 0, f["faibles"], n)["gemini"]
        self.assertNotEqual((k, g), (0, 0))
        self.assertEqual([e["kraken", c] for c in ("BTC", "ETH", "USDC", "USDT")], [(k, 0)] * 4)
        self.assertEqual([e["gemini", c] for c in ("BTC", "ETH", "USDC", "USDT")], [(0, g)] + [(0, 0)] * 3)
        f["faibles"] = dict(f["faibles"], type="panne")
        e = sources.Replication(PRM, EP, f, "T-E", 0, m, n).etat()
        self.assertEqual([e["gemini", c] for c in ("BTC", "ETH", "USDC", "USDT")], [(g, 0)] * 4)
        f["faibles"] = dict(f["faibles"], type="autre")
        with self.assertRaises(commun.Refus) as c:
            sources.Replication(PRM, EP, f, "T-E", 0, m, n).etat()
        self.assertEqual(c.exception.code, "SOURCES/faible")


class TestCasG2(unittest.TestCase):
    """C-1 de la G2 de la tranche 2, (a) à (j) : un cas écrit à la main par mutant resté vivant (R-01 à R-09, R-19,
    R-22, R-25 du réviseur), vert sur le code et rouge sous son mutant ; repris des prototypes du réviseur."""

    def test_faibles_independantes(self):
        """(a) Deux unités faibles, p = 1/2, L = 1 : P(les deux) = 1/4 à 5 SE sur 60 réplications de 400 fenêtres (un
        flux commun donnerait 1/2). Mutation R-01 : un seul flux pour toutes les unités faibles."""
        spec, x = {"hotes": ["gemini", "kraken"], "p": Fraction(1, 2), "L": 1, "type": "panne"}, []
        for i in range(60):
            e = sources.faibles(PRM, "T-C1A", i, spec, 400)
            x.append(part(e["gemini"] & e["kraken"], 0, 400))
        self.assertTrue(dans_5_se(x, Fraction(1, 4)))

    def test_ecarts_independants_par_classe(self):
        """(b) EP d'essai (binance calme : 2 830 cellules d'écart pour 372 de panne, écart propre p = 2 458/24 585),
        f = 1, τ = 0 : F(binance, BTC) ≠ F(binance, ETH) et P(les deux) = p² à 5 SE sur 60 réplications de 2 000
        fenêtres. Mutation R-02 : composantes d'écart de toutes les classes sur l'emplacement 0."""
        ep = dict(EP)
        ep["calme", "binance", "ecart"] = dict(EP["calme", "binance", "ecart"], cellules=2830)
        m, x = {"calme": (1 << 2000) - 1, "stress": 0}, []
        for i in range(60):
            r = sources.Replication(PRM, ep, fond(), "T-C1B", i, m, 2000)
            a, b = r.ecarts("binance", 0), r.ecarts("binance", 1)
            self.assertNotEqual(a, b)
            x.append(part(a & b, 0, 2000))
        self.assertTrue(dans_5_se(x, Fraction(2458, 24585) * Fraction(2458, 24585)))

    def test_sens_des_tendances_et_de_la_commune(self):
        """(c) Sens tirés à la main, croissant si u < 1/2. « tendances » : un tirage par hôte dans l'ordre du pool (0,2
        et 0,7 alternés) ; « commune » : un seul tirage (0,7 : décroissant) pour les dix hôtes, les douze valeurs
        suivantes restant inemployées. Mutations R-03 (commune : un sens par hôte), R-04 (tendances : un seul sens)."""
        lo, hi, tous = Fraction(1, 10), Fraction(19, 10), [h for h, _f in PRM["calibration"]["unites"]]
        d = sources.derives(PRM, {"genres": ["tendances"], "duree": 100}, suite(*[0.2, 0.7] * 5))["specs"]
        self.assertEqual([d[h] for h in tous], [("lineaire", lo, hi, 100), ("lineaire", hi, lo, 100)] * 5)
        reste = iter([0.7] + [0.2] * 12)
        d = sources.derives(PRM, {"genres": ["commune"], "duree": 100}, reste.__next__)["specs"]
        self.assertEqual(([d[h] for h in tous], len(list(reste))), ([("lineaire", hi, lo, 100)] * 10, 12))

    def test_regime_par_strate(self):
        """(d) Z(binance, calme) et Z(binance, stress) sur des flux distincts : φ = 1/5 en calme, 1/20 en stress (κ = 3,
        τ_D = 20) ; 150 réplications de 2 000 fenêtres : parts à 5 SE de 1/5 et de 1/20 ; à φ égal, les deux masques
        diffèrent. Mutation R-05 : régime partagé entre strates (clé de cache sans la strate)."""
        m = {"calme": (1 << 2000) - 1, "stress": (1 << 2000) - 1}
        reg = {"calme": (Fraction(1, 5), Fraction(3), 20), "stress": (Fraction(1, 20), Fraction(3), 20)}
        z = [sources.Replication(PRM, EP, dict(fond(), regime=reg), "T-C1D", i, m, 2000) for i in range(150)]
        self.assertTrue(dans_5_se([part(r.regime("binance", "calme"), 0, 2000) for r in z], Fraction(1, 5)))
        self.assertTrue(dans_5_se([part(r.regime("binance", "stress"), 0, 2000) for r in z], Fraction(1, 20)))
        r = sources.Replication(PRM, EP, fond(regime=reg["calme"]), "T-C1D", 0, m, 2000)
        self.assertNotEqual(r.regime("binance", "calme"), r.regime("binance", "stress"))

    def test_paire_imposant_un_candidat(self):
        """(e) Paire parmi les 7 hôtes AS13335 imposant kraken, qui en est membre : kraken (v = 0), puis 0,84 parmi les
        six autres (seuils j/6 : rang 5, okx) ; parmi les sept (seuils j/7), 0,84 redonnerait kraken. Mutation R-06 :
        imposé non retiré des candidats."""
        self.assertEqual(sources.touches(PRM, suite(0.0, 0.84), ("parmi", AS, 2, ["kraken"])), ["kraken", "okx"])

    def test_depart_stationnaire_epingle(self):
        """(f) Loi 1×1 3×1 (moyenne 2), q = 1/2 : départ en cours si u < μq/(μq + 1) = 1/2 ; u = 0,49 : en cours (reste
        1 à u = 0,1, pause 1, durée 1) ; la moyenne 7/4 de la loi résiduelle donnerait le seuil 7/15 < 0,49 ; u = 0,5
        hors épisode (test_alterner_pas_a_pas). Mutation R-07 : seuil calculé sur la moyenne de la loi résiduelle."""
        loi = sources.Empirique([(1, 1), (3, 1)])
        self.assertEqual(sources.alterner(suite(0.49, 0.1, 0.1, 0.1), loi, Fraction(1, 2), A, 3), [(0, 1), (2, 3)])

    def test_panne_initiale_bornee_par_l_horizon(self):
        """(g) Horizon de 1 000 fenêtres, sous les 4 320 de la panne initiale, f = 0 : les pannes de l'hôte tiré valent
        exactement (1 << 1 000) − 1. Mutation R-08 : panne initiale non bornée par l'horizon."""
        f = dict(fond("0"), derive={"genres": ["initiale"], "duree": 1440})
        r = sources.Replication(PRM, EP, f, "T-C1G", 0, {"calme": (1 << 1000) - 1, "stress": 0}, 1000)
        self.assertEqual(r.pannes(r.derives()["initiale"]), (1 << 1000) - 1)

    def test_transitoire_exclusif(self):
        """(h) Le transitoire est un multiplicateur : avec les tendances, la tendance commune ou les sauts,
        SOURCES/derive. Mutation R-09 : exclusivité contrôlée sur les trois premiers genres seulement."""
        for g in (["transitoire", "tendances"], ["commune", "transitoire"], ["sauts", "transitoire"]):
            with self.assertRaises(commun.Refus) as c:
                sources.derives(PRM, {"genres": g, "duree": 1440}, suite(*[0.1] * 20))
            self.assertEqual(c.exception.code, "SOURCES/derive", g)

    def test_lois_ecart_et_regroupee(self):
        """(i) EP d'essai à histogrammes distinctifs, f = 1, τ = 0, 10 réplications de 4 000 fenêtres ; épisodes entiers
        (ni à 0 ni à l'horizon). F suit la loi « ecart » : binance calme, 2 830 cellules d'écart, histogramme 4×100 :
        longueur 4 seule. H en stress suit la loi regroupée (1×662 2×11) : histogramme « panne » de binance calme mis à
        7×100, strate stress seule : longueurs 1 et 2 seules. Mutations R-19 (F tiré avec la loi « panne »), R-22 (H de
        la strate tirée avec la loi du calme)."""
        ep, n, f, h = dict(EP), 4000, set(), set()
        ep["calme", "binance", "ecart"] = dict(EP["calme", "binance", "ecart"], cellules=2830, histogramme=((4, 100),))
        ep["calme", "binance", "panne"] = dict(EP["calme", "binance", "panne"], histogramme=((7, 100),))
        for i in range(10):
            r = sources.Replication(PRM, ep, fond(), "T-C1I", i, {"calme": (1 << n) - 1, "stress": 0}, n)
            f |= {b - a for a, b in calendrier.segments(r.ecarts("binance", 0)) if 0 < a and b < n}
            r = sources.Replication(PRM, ep, fond(), "T-C1I", i, {"calme": 0, "stress": (1 << n) - 1}, n)
            h |= {b - a for a, b in calendrier.segments(r.pannes("binance")) if 0 < a and b < n}
        self.assertEqual(f, {4})
        self.assertTrue(h and h <= {1, 2}, h)

    def test_ecart_faible_hors_panne(self):
        """(j) Fond f = 1, incidents sur gemini (ρ = 144 par jour, D = 5, π = 1), unité faible gemini de type « ecart »
        (p = 1/2, L = 1) : le masque faible recouvre la panne, l'écart de gemini en BTC jamais. Mutation R-25 : écart
        faible ajouté hors de la clause « hors panne »."""
        f = dict(fond(), faibles={"hotes": ["gemini"], "p": Fraction(1, 2), "L": 1, "type": "ecart"},
                 incidents=inc(144, 5, ("chacun", ["gemini"], Fraction(1))))
        e = sources.Replication(PRM, EP, f, "T-C1J", 0, {"calme": (1 << 4000) - 1, "stress": 0}, 4000).etat()
        g = sources.faibles(PRM, "T-C1J", 0, f["faibles"], 4000)["gemini"]
        self.assertNotEqual(g & e["gemini", "BTC"][0], 0)
        self.assertEqual(e["gemini", "BTC"][0] & e["gemini", "BTC"][1], 0)
