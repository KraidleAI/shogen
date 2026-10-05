"""Observateurs SB-6 (E-S-17 à E-S-22 ; T-OBS-1, T-OBS-2) : tables de votes et de validité écrites à la main, fenêtre
par fenêtre (bit j = fenêtre j) ; chaque test nomme les mutations qui le rougissent."""
import unittest
from fractions import Fraction

import aleas
import calendrier
import calibration
import commun
import observateurs
import sources

PRM = commun.charger_parametres(environ={})
EP = calibration.charger(PRM, environ={})["episodes"]


def dans_5_se(x: list, r: Fraction) -> bool:
    """Moyenne des rationnels x à moins de 5 erreurs-types de r : (x̄ − r)² < 25·s²/R, s² variance sans biais."""
    m = sum(x, Fraction(0)) / len(x)
    s2 = sum(((y - m) * (y - m) for y in x), Fraction(0)) / (len(x) - 1)
    return (m - r) * (m - r) < 25 * s2 / len(x)


def bits(*positions) -> int:
    """Masque des fenêtres données."""
    m = 0
    for p in positions:
        m |= 1 << p
    return m


class TestQuorum(unittest.TestCase):
    def test_parametres(self):
        """Section observateurs (E-S-17 à E-S-21), recopiée à la main : M = 4, O1 à O3 dans l'UE, O4 absent au repli,
        paires de 60 fenêtres, artefacts de 20, défaut local de durée moyenne 2, absences de 5, 180 et 4 320 fenêtres à
        poids égaux ; composants en liste fermée, disjointe de celle des sources ; composant non déclaré :
        OBSERVATEURS/composant. Mutation M-6A-01 : contrôle du composant retiré."""
        o = PRM["observateurs"]
        self.assertEqual((o["M"], o["ue"], o["repli"], o["duree_paire"], o["duree_artefact"], o["duree_locale"],
                          o["absences"]), (4, [0, 1, 2], 3, 60, 20, 2, [[5, 1], [180, 1], [4320, 1]]))
        self.assertEqual(set(o["composants"]) & set(PRM["sources"]["composants"]), set())
        self.assertEqual(observateurs.flux(PRM, "N1", 0, "obs-local", 2)(),
                         aleas.flux(PRM["aleas"], "N1", 0, "obs-local", 2)())
        with self.assertRaises(commun.Refus) as c:
            observateurs.flux(PRM, "N1", 0, "panne", 0)
        self.assertEqual(c.exception.code, "OBSERVATEURS/composant")

    def test_quorum_t_obs_1(self):
        """T-OBS-1, table écrite à la main, une fenêtre par entrée « valides/votants → D » : f0 0123/012 → 1 (3 sur
        4) ; f1 0123/01 → 0 ; f2 012/01 → 1 (2 sur 3) ; f3 012/0, plus le vote de 3, non valide → 0 ; f4 01/01 → 1 (2
        sur 2) ; f5 01/0 → 0 ; f6 0/0 → 0 (M_j = 1, non évaluable) ; f7 aucun/0123 → 0 ; f8 0123/0123 → 1 ; f9 123/123
        → 1 ; f10 23/aucun → 0 ; f11 0123/3 → 0. Évaluables : f0 à f5 et f8 à f11 ; M_j = 4 en f0, f1, f8, f11.
        Comptage par plans : fenêtres 0, 1, 2 à 1, 3 et 1 masques ; huit masques : OBSERVATEURS/compte. Mutations
        M-OBS-1 (q = 2 fixe), M-OBS-2 (q = ⌈M_j/2⌉), M-OBS-3 (non valide compté comme votant), M-6A-02 (M_j = 1
        évaluable), M-6A-08 (garde des huit masques retirée), M-6A-09 (bit du nombre inversé), M-6A-10 (retenue
        perdue)."""
        g = (1 << 12) - 1
        valides = [bits(0, 1, 2, 3, 4, 5, 6, 8, 11), bits(0, 1, 2, 3, 4, 5, 8, 9, 11), bits(0, 1, 2, 3, 8, 9, 10, 11),
                   bits(0, 1, 8, 9, 10, 11)]
        votes = [bits(0, 1, 2, 3, 4, 5, 6, 7, 8), bits(0, 1, 2, 4, 7, 8, 9), bits(0, 7, 8, 9), bits(3, 7, 8, 9, 11)]
        q = observateurs.Quorum(valides, g)
        self.assertEqual(q.evaluables, bits(0, 1, 2, 3, 4, 5, 8, 9, 10, 11))
        self.assertEqual(q.nombre[4], bits(0, 1, 8, 11))
        self.assertEqual(q.atteint(votes), bits(0, 2, 4, 8, 9))
        self.assertEqual(observateurs.compter([bits(0, 1), bits(1), bits(1, 2)]), [bits(0, 1, 2), bits(1), 0])
        with self.assertRaises(commun.Refus) as c:
            observateurs.compter([1] * 8)
        self.assertEqual(c.exception.code, "OBSERVATEURS/compte")

    def test_vote_tout_axe_et_ok(self):
        """E-S-19, E-S-22, à la main, quatre observateurs valides sur 6 fenêtres, séries (kraken, ETH) et (kraken, BTC)
        : panne vraie de l'hôte en 0 et 1, écart vrai (hors panne) en 2 et 3. Fenêtre 0 : O3 et O4 ne voient pas la
        panne (régionale) : 2 votes → D = 0 ; ok = 0 (deux non panne). Fenêtre 1 : O3 et O4 la manquent (β, par hôte) :
        D = 0, ok = 0. Fenêtre 2 : O3 et O4 manquent l'écart d'ETH (β, par classe) : D = 0 en ETH, D = 1 en BTC ; ok = 1
        (un écart porte un prix : statut non panne). Fenêtre 3 : D = 1, ok = 1. Fenêtre 4 : chemins de O1 à O3 en échec
        (ε) : D = 1, ok = 0. Fenêtre 5 : rien : D = 0, ok = 1. Sans vues : D = {0, 1, 2, 3}, ok = {2, 3, 4, 5}.
        Mutations M-6A-03 (manque de panne ignoré), M-6A-04 (écart vu compté comme statut panne), M-6A-05 (panne
        régionale ignorée), M-6A-07 (manque d'écart appliqué à toutes les classes)."""
        q = observateurs.Quorum([(1 << 6) - 1] * 4, (1 << 6) - 1)
        etat = {("kraken", "ETH"): (bits(0, 1), bits(2, 3)), ("kraken", "BTC"): (bits(0, 1), bits(2, 3))}
        vues = {("cache", 2, "kraken"): bits(0), ("cache", 3, "kraken"): bits(0), ("manque", 2, "kraken"): bits(1),
                ("manque", 3, "kraken"): bits(1), ("manque", 2, "kraken", "ETH"): bits(2),
                ("manque", 3, "kraken", "ETH"): bits(2)}
        vues.update({("chemin", o, "kraken"): bits(4) for o in (0, 1, 2)})
        self.assertEqual(observateurs.consolider(etat, q, vues), {("kraken", "ETH"): (bits(3, 4), bits(2, 3, 5)),
                                                                  ("kraken", "BTC"): (bits(2, 3, 4), bits(2, 3, 5))})
        self.assertEqual(observateurs.consolider(etat, q, {}), {k: (bits(0, 1, 2, 3), bits(2, 3, 4, 5)) for k in etat})

    def test_defaut_local_t_obs_2(self):
        """T-OBS-2, à la main : état vrai nul sur les 38 séries (10 + 10 + 8 + 10) ; chemins en échec sur les dix hôtes
        : O2 en fenêtres 1 et 2, O3 en fenêtre 1 ; O1 en défaut local (E-S-20) en fenêtres 1 et 2 : il vote « panne »
        pour toutes les unités de toutes les classes, ce qui abaisse d'un vote le quorum de chacune. Avec le défaut : D
        = {1} (3 votes sur 4) et ok = {0, 3} sur les 38 séries ; sans : D = 0 (2 votes) et ok = {0, 2, 3}. Mutations
        M-OBS-4 (défaut appliqué à la seule première classe), M-6A-06 (défaut local hors des statuts « panne »)."""
        q = observateurs.Quorum([(1 << 4) - 1] * 4, (1 << 4) - 1)
        etat = {(h, c): (0, 0) for c, pool in sources.classes(PRM) for h in pool}
        vues = {}
        for h, _f in PRM["calibration"]["unites"]:
            vues.update({("chemin", 1, h): bits(1, 2), ("chemin", 2, h): bits(1)})
        self.assertEqual(len(etat), 38)
        self.assertEqual(observateurs.consolider(etat, q, {**vues, ("local", 0): bits(1, 2)}),
                         {k: (bits(1), bits(0, 3)) for k in etat})
        self.assertEqual(observateurs.consolider(etat, q, vues), {k: (0, bits(0, 2, 3)) for k in etat})


def suite(*u):
    """u() qui rend les valeurs données, dans l'ordre (StopIteration au-delà)."""
    return iter(u).__next__


def couche(**k) -> dict:
    """Couche d'essai (E-S-17, E-S-18) : rien par défaut ; k remplace."""
    return dict({"absences": Fraction(0), "degradations": Fraction(0), "paires": Fraction(0), "perte": None,
                 "repli": False, "chemin": None, "local": Fraction(0), "artefacts": Fraction(0),
                 "regionale": Fraction(0), "manque": Fraction(0)}, **k)


def part(m: int, n: int) -> Fraction:
    return Fraction(m.bit_count(), n)


class TestValidite(unittest.TestCase):
    def test_paires_pas_a_pas(self):
        """Pannes de paires (Q-S-11) à la main : ρ = 720 par jour, soit 1/2 par fenêtre (seuils 1/2, 3/4, 7/8, …), durée
        2 au lieu de 60 (paramètre d'essai), horizon 8 : débuts en 0 (u = 0,3) et 3 (0,8), pause 5 au-delà (0,95) ;
        paires parmi les six de {O1..O4} dans l'ordre (01, 02, 03, 12, 13, 23) : v = 0,5 → 12, v = 0,1 → 01. O1 non
        valide en 3 et 4, O2 en 0, 1, 3, 4, O3 en 0 et 1, O4 toujours valide. Repli M = 3 (E-S-18) : O4 jamais valide ;
        débuts en 0 et 7 (0,3 ; 0,99), paires parmi les trois de {O1..O3} (01, 02, 12) : v = 0,5 → 02, v = 0,9 → 12.
        Mutations M-6B-01 (durée de paire constante, 60, au lieu du paramètre), M-6B-02 (paire tirée parmi les quatre
        au repli), M-6B-03 (repli ignoré)."""
        prm = dict(PRM, observateurs=dict(PRM["observateurs"], duree_paire=2))
        g, essais = (1 << 8) - 1, {("obs-paires", 0): suite(0.3, 0.8, 0.95), ("obs-paires", 1): suite(0.5, 0.1)}
        v = observateurs.Couche(prm, couche(paires=Fraction(720)), "T-6B", 0, 8, essais).validites()
        self.assertEqual(v, [g & ~bits(3, 4), g & ~bits(0, 1, 3, 4), g & ~bits(0, 1), g])
        essais = {("obs-paires", 0): suite(0.3, 0.99), ("obs-paires", 1): suite(0.5, 0.9)}
        v = observateurs.Couche(prm, couche(paires=Fraction(720), repli=True), "T-6B", 0, 8, essais).validites()
        self.assertEqual(v, [g & ~bits(0, 1), g & ~bits(7), g & ~bits(0, 1, 7), 0])

    def test_perte_definitive(self):
        """Perte d'un observateur à un instant tiré (E-S-17, N5), sur 2 880 fenêtres nominales (deux jours) :
        observateur parmi les quatre (u = 0,6 → O3), jour (0,3 → 0), fenêtre du jour (0,25 → 360) : O3 non valide de la
        fenêtre 360 à l'horizon (3 000), plus d'un jour ; au repli, parmi les trois présents (0,6 → O2). Durée non
        multiple d'un jour : OBSERVATEURS/perte. Mutations M-6B-04 (instant : jour et fenêtre permutés), M-6B-05 (perte
        bornée à un jour)."""
        g = (1 << 3000) - 1
        v = observateurs.Couche(PRM, couche(perte=2880), "T-6B", 0, 3000, {("obs-perte", 0): suite(0.6, 0.3, 0.25)})
        v = v.validites()
        self.assertEqual(v, [g, g, (1 << 360) - 1, g])
        v = observateurs.Couche(PRM, couche(perte=2880, repli=True), "T-6B", 0, 3000,
                                {("obs-perte", 0): suite(0.6, 0.3, 0.25)}).validites()
        self.assertEqual(v, [g, (1 << 360) - 1, g, 0])
        with self.assertRaises(commun.Refus) as c:
            observateurs.Couche(PRM, couche(perte=1000), "T-6B", 0, 3000).validites()
        self.assertEqual(c.exception.code, "OBSERVATEURS/perte")

    def test_absences_et_degradations(self):
        """Absences D-1 (renouvellement stationnaire, longueurs d'essai 2 et 5 à poids égaux) de part 1/20 et
        dégradations D-2 à D-5 (tirages indépendants par fenêtre) de part 1/10 ; 100 réplications de 4 000 fenêtres :
        part non valide de O1 à 5 SE de 1 − (19/20)(9/10) = 29/200 ; O1 et O2 non valides ensemble à 5 SE de
        (29/200)², flux propres à chaque observateur ; absences seules : épisodes entiers de longueur 2 ou 5 seulement ;
        dégradations seules : des épisodes d'une fenêtre.
        Mutations M-6B-06 (absences omises), M-6B-07 (flux commun aux observateurs), M-6B-08 (dégradations en
        épisodes de la loi des absences)."""
        prm = dict(PRM, observateurs=dict(PRM["observateurs"], absences=[[2, 1], [5, 1]]))
        x, y, lg, ld, n = [], [], set(), set(), 4000
        for i in range(100):
            v = observateurs.Couche(prm, couche(absences=Fraction(1, 20), degradations=Fraction(1, 10)), "T-6B", i,
                                    n).validites()
            x.append(1 - part(v[0], n))
            y.append(part(((1 << n) - 1) & ~(v[0] | v[1]), n))
            a = observateurs.Couche(prm, couche(absences=Fraction(1, 20)), "T-6B", i, n).validites()[2]
            lg |= {b - d for d, b in calendrier.segments(((1 << n) - 1) & ~a) if 0 < d and b < n}
            a = observateurs.Couche(prm, couche(degradations=Fraction(1, 10)), "T-6B", i, n).validites()[2]
            ld |= {b - d for d, b in calendrier.segments(((1 << n) - 1) & ~a) if 0 < d and b < n}
        self.assertTrue(dans_5_se(x, Fraction(29, 200)))
        self.assertTrue(dans_5_se(y, Fraction(29, 200) * Fraction(29, 200)))
        self.assertEqual(lg, {2, 5})
        self.assertIn(1, ld)

    def test_loi_des_absences_parametres(self):
        """C-2 (c) de la G2 de la tranche 3 (E-S-17 ; Q-T3-2) : la loi des absences de parametres.json (5, 180 et 4 320
        fenêtres, poids égaux) est celle que tire Couche.validites : absences de part 1/2, 40 réplications de 20 000
        fenêtres, quatre observateurs ; longueurs des épisodes entiers (ni coupés à 0 ni à l'horizon) = {5, 180, 4 320}
        exactement. Mutation V-20 du réviseur (loi réduite à ses deux premières longueurs)."""
        lg, n = set(), 20000
        for i in range(40):
            for v in observateurs.Couche(PRM, couche(absences=Fraction(1, 2)), "T-C2", i, n).validites():
                lg |= {b - a for a, b in calendrier.segments(((1 << n) - 1) & ~v) if 0 < a and b < n}
        self.assertEqual(lg, {5, 180, 4320})


class TestVotes(unittest.TestCase):
    def test_chemins_epsilon(self):
        """Échecs de chemin seuls (E-S-19, Q-S-12) : référence ε_u = (1 − f)·p̂_u, p̂_u = cellules d'écart/n_s d'EP :
        binance calme à f = 3/10, (7/10)·372/24 585 = 434/40 975 (EP l.15), bitfinex calme (7/10)·32/24 585 =
        112/122 925 (EP l.19 : 32 cellules d'écart pour 30 de panne). ε = 1/10 pour binance en calme, 0 en
        stress (grille de 2 × 2 000 fenêtres) ; 60 réplications : part de O1 en calme à 5 SE de 1/10, aucune en
        stress ; O1 et O2 ensemble à 5 SE de 1/100 (indépendance par observateur) ; pool à rebours : masques
        identiques (indices ancrés sur sources.indices_hotes). Mutations M-6C-01 (masque de strate omis), M-6C-02
        (flux commun aux observateurs), M-6C-03 (référence sur la ligne « panne »), M-6C-12 (f omis)."""
        ref = observateurs.chemin_reference(PRM, EP, Fraction(3, 10))
        self.assertEqual((ref["binance", "calme"], ref["bitfinex", "calme"], len(ref)),
                         (Fraction(434, 40975), Fraction(112, 122925), 20))
        n, m = 4000, {"calme": (1 << 2000) - 1, "stress": ((1 << 2000) - 1) << 2000}
        eps, x, y = {("binance", "calme"): Fraction(1, 10), ("binance", "stress"): Fraction(0)}, [], []
        rebours = dict(PRM, calibration=dict(PRM["calibration"], unites=list(reversed(PRM["calibration"]["unites"]))))
        for i in range(60):
            v = observateurs.Couche(PRM, couche(chemin=eps), "T-6C", i, n).vues({}, m)
            self.assertEqual(v[("chemin", 0, "binance")] >> 2000, 0)
            x.append(part(v[("chemin", 0, "binance")], 2000))
            y.append(part(v[("chemin", 0, "binance")] & v[("chemin", 1, "binance")], 2000))
            if i < 3:
                self.assertEqual(observateurs.Couche(rebours, couche(chemin=eps), "T-6C", i, n).vues({}, m), v)
        self.assertTrue(dans_5_se(x, Fraction(1, 10)))
        self.assertTrue(dans_5_se(y, Fraction(1, 100)))

    def test_defauts_locaux_et_artefacts(self):
        """Défaut local (E-S-20) : part stationnaire λ = 1/20, épisodes géométriques de moyenne 2 ; 100 réplications de
        4 000 fenêtres : part de O3 à 5 SE de 1/20, longueur moyenne des épisodes entiers à 5 SE de 2. Artefacts
        (E-S-21) à la main : ρ = 720 par jour (1/2 par fenêtre), durée 2 au lieu de 20 (paramètre d'essai), horizon 8 :
        débuts en 0 et 3 (u = 0,3 ; 0,8 ; 0,95), soit les fenêtres 0, 1, 3, 4, pour O1 à O3 (UE) sur les 7 hôtes
        AS13335, rien pour O4 ni pour binance, bitstamp, gemini. Mutations M-6C-04 (λ pris comme taux de débuts),
        M-6C-05 (épisodes de défaut local d'une fenêtre), M-6C-06 (artefacts pour les quatre observateurs), M-6C-07
        (artefacts sur tous les hôtes)."""
        x, lg, n = [], [], 4000
        for i in range(100):
            v = observateurs.Couche(PRM, couche(local=Fraction(1, 20)), "T-6C", i, n).vues({}, {})
            x.append(part(v[("local", 2)], n))
            lg += [Fraction(b - a) for a, b in calendrier.segments(v[("local", 2)]) if 0 < a and b < n]
        self.assertTrue(dans_5_se(x, Fraction(1, 20)))
        self.assertTrue(dans_5_se(lg, Fraction(2)))
        prm = dict(PRM, observateurs=dict(PRM["observateurs"], duree_artefact=2))
        v = observateurs.Couche(prm, couche(artefacts=Fraction(720)), "T-6C", 0, 8,
                                {("obs-artefacts", 0): suite(0.3, 0.8, 0.95)}).vues({}, {})
        attendu = {("artefact", o, h): bits(0, 1, 3, 4) for o in (0, 1, 2) for h in PRM["sources"]["as13335"]}
        self.assertEqual({k: w for k, w in v.items() if w}, attendu)

    def test_artefacts_consolides_e_s_21(self):
        """C-2 (a) de la G2 de la tranche 3 (E-S-21, E-S-22), à la main sur 4 fenêtres, état vrai nul : O1 à O3 en
        artefact sur kraken (AS13335) en fenêtres 1 et 2, binance intact. M_j = 4 (q_j = 3) : trois statuts « panne »,
        donc trois votes → D(kraken) = {1, 2} ; en 1 et 2, un seul statut non panne (O4) → ok(kraken) = {0, 3} ; binance
        : D = 0, ok = {0, 1, 2, 3}. Repli (O4 non valide, M_j = 3, q_j = 2) : même résultat. Couche.consolidation,
        artefacts d'essai (ρ = 720 par jour, durée 2, débuts en 0 et 3 : u = 0,3 ; 0,8 ; 0,95, comme ci-dessus), horizon
        8 : D = {0, 1, 3, 4} et ok = {2, 5, 6, 7} sur les 7 hôtes AS13335 ; D = 0 et ok = {0, …, 7} sur binance,
        bitstamp et gemini. Mutations V-02 (artefact hors du calcul de « ok ») et V-25 (artefact hors du statut
        « panne ») du réviseur."""
        etat = {("kraken", "BTC"): (0, 0), ("binance", "BTC"): (0, 0)}
        vues = {("artefact", o, "kraken"): bits(1, 2) for o in (0, 1, 2)}
        attendu = {("kraken", "BTC"): (bits(1, 2), bits(0, 3)), ("binance", "BTC"): (0, bits(0, 1, 2, 3))}
        for valides in ([15] * 4, [15, 15, 15, 0]):
            self.assertEqual(observateurs.consolider(etat, observateurs.Quorum(valides, 15), vues), attendu, valides)
        prm = dict(PRM, observateurs=dict(PRM["observateurs"], duree_artefact=2))
        etat = {(h, "BTC"): (0, 0) for h, _f in PRM["calibration"]["unites"]}
        _q, s = observateurs.Couche(prm, couche(artefacts=Fraction(720)), "T-C2", 0, 8,
                                    {("obs-artefacts", 0): suite(0.3, 0.8, 0.95)}).consolidation(etat, {})
        as13335 = PRM["sources"]["as13335"]
        self.assertEqual({h: x for (h, _c), x in s.items()},
                         {h: (bits(0, 1, 3, 4), bits(2, 5, 6, 7)) if h in as13335 else (0, 255)
                          for h, _f in PRM["calibration"]["unites"]})

    def test_regionale_et_manques(self):
        """À la main, panne vraie de kraken (BTC et ETH) en 1, 2, 5, 6, 7, écart d'ETH en 3. Panne régionale (π = 1/2,
        flux « obs-regionale » d'indice 2, rang de kraken) : épisode [1, 3) régional (u = 0,3), vu par le sous-ensemble
        d'indice 7 des 14 sous-ensembles propres non vides, rangés par masque (u = 0,5 → masque 8, O4 seul) : cache pour
        O1 à O3 ; épisode [5, 8) régional (0,2), sous-ensemble d'indice 13 (0,95 → masque 14, O2 à O4) : cache pour O1.
        Consolidation : D = {5, 6, 7} (la panne vue d'un seul point est censurée, celle de trois points comptée), ok =
        {0, 1, 2, 3, 4} (O1 à O3, qui ne voient pas la première, ont un statut non panne). Manques β = 1/2, sur
        une panne de kraken en 2 et 5 et un écart d'ETH en 3 : par hôte (flux « obs-manque » 20), fenêtre 2, u = 0,3,
        0,7, 0,2, 0,9 → O1, O3 ; fenêtre 5, 0,6, 0,1, 0,8, 0,4 → O2, O4 ; par classe (flux 22 pour ETH, aucun tirage
        pour BTC, sans écart) : fenêtre 3, 0,9, 0,9, 0,1, 0,9 → O3. Mutations M-6C-08 (cache donné aux observateurs du
        sous-ensemble), M-6C-09 (manque d'écart sur le flux de l'hôte), M-6C-10 (sous-ensemble plein admis)."""
        etat = {("kraken", "BTC"): (bits(1, 2, 5, 6, 7), 0), ("kraken", "ETH"): (bits(1, 2, 5, 6, 7), bits(3))}
        reg = observateurs.Couche(PRM, couche(regionale=Fraction(1, 2)), "T-6C", 0, 8,
                                  {("obs-regionale", 2): suite(0.3, 0.5, 0.2, 0.95)}).vues(etat, {})
        self.assertEqual({k: w for k, w in reg.items() if w}, {("cache", 0, "kraken"): bits(1, 2, 5, 6, 7),
                                                               ("cache", 1, "kraken"): bits(1, 2),
                                                               ("cache", 2, "kraken"): bits(1, 2)})
        self.assertEqual(observateurs.consolider(etat, observateurs.Quorum([255] * 4, 255), reg),
                         {("kraken", "BTC"): (bits(5, 6, 7), bits(0, 1, 2, 3, 4)),
                          ("kraken", "ETH"): (bits(3, 5, 6, 7), bits(0, 1, 2, 3, 4))})
        etat = {("kraken", "BTC"): (bits(2, 5), 0), ("kraken", "ETH"): (bits(2, 5), bits(3))}
        essais = {("obs-manque", 20): suite(0.3, 0.7, 0.2, 0.9, 0.6, 0.1, 0.8, 0.4),
                  ("obs-manque", 22): suite(0.9, 0.9, 0.1, 0.9)}
        man = observateurs.Couche(PRM, couche(manque=Fraction(1, 2)), "T-6C", 0, 8, essais).vues(etat, {})
        self.assertEqual({k: w for k, w in man.items() if w},
                         {("manque", 0, "kraken"): bits(2), ("manque", 2, "kraken"): bits(2),
                          ("manque", 1, "kraken"): bits(5), ("manque", 3, "kraken"): bits(5),
                          ("manque", 2, "kraken", "ETH"): bits(3)})

    def test_observateurs_parfaits(self):
        """Oracle exact (E-S-22) : sans bruit d'observateur (quatre valides, ni ε, ni défaut, ni artefact, ni manque),
        la consolidation rend l'état vrai : D = panne | écart et ok = non panne, pour les 38 séries d'une réplication
        (f = 1, τ = 1/50, 2 000 fenêtres) ; fenêtres toutes évaluables ; au repli M = 3, de même, toutes les fenêtres
        à M_j = 3. Mutation M-6C-11 : validités ignorées par la consolidation."""
        n, m = 2000, {"calme": (1 << 2000) - 1, "stress": 0}
        fond = {"f": Fraction(1), "regime": {"calme": None, "stress": None}, "longues": Fraction(0),
                "autres": Fraction(1), "hors_enveloppe": Fraction(1, 50)}
        etat = sources.Replication(PRM, EP, fond, "T-6C", 0, m, n).etat()
        q, series = observateurs.Couche(PRM, couche(), "T-6C", 0, n).consolidation(etat, m)
        self.assertEqual(q.evaluables, (1 << n) - 1)
        self.assertEqual(series, {k: (p | e, ((1 << n) - 1) & ~p) for k, (p, e) in etat.items()})
        self.assertNotEqual({p for p, _e in etat.values()}, {0})
        q, s3 = observateurs.Couche(PRM, couche(repli=True), "T-6C", 0, n).consolidation(etat, m)
        self.assertEqual((q.nombre[3], s3), ((1 << n) - 1, series))
