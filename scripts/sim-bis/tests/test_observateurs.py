"""Observateurs SB-6 (E-S-17 à E-S-22 ; T-OBS-1, T-OBS-2) : tables de votes et de validité écrites à la main, fenêtre
par fenêtre (bit j = fenêtre j) ; chaque test nomme les mutations qui le rougissent."""
import unittest
from fractions import Fraction

import aleas
import calendrier
import commun
import observateurs
import sources

PRM = commun.charger_parametres(environ={})


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
                 "repli": False}, **k)


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
