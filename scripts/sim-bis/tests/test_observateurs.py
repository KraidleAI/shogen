"""Observateurs SB-6 (E-S-17 à E-S-22 ; T-OBS-1, T-OBS-2) : tables de votes et de validité écrites à la main, fenêtre
par fenêtre (bit j = fenêtre j) ; chaque test nomme les mutations qui le rougissent."""
import unittest

import aleas
import commun
import observateurs
import sources

PRM = commun.charger_parametres(environ={})


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
