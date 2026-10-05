"""Aléas SB-1 (E-S-41, E-S-42, E-S-43 ; T-AL-1, T-AL-2) : graines par `sha256sum` et `bc` (8 premiers octets en
décimal), seuils caractérisés en `Fraction` (plus petit flottant ≥ la valeur exacte) ; chaque test nomme les mutations
qui le rougissent. Aucun tirage n'est jugé à l'œil : les frontières se testent avec des u écrits à la main."""
import math
import random
import unittest
from fractions import Fraction

import aleas
import commun

A = commun.charger_parametres(environ={})["aleas"]


def suite(*u):
    """u() qui rend les valeurs données, dans l'ordre."""
    return iter(u).__next__


class TestAleas(unittest.TestCase):
    def refus(self, code, f, *a):
        with self.assertRaises(commun.Refus) as c:
            f(*a)
        self.assertEqual(c.exception.code, code)

    def test_parametres(self):
        """GRAINE fixée par le G0 (E-S-41), préfixe, rangs et bits de garde de parametres.json."""
        self.assertEqual(A, {"prefixe": "SHOGEN-SIM-BIS", "graine": 20261004, "rangs": 4096, "garde": 128,
                             "source": A["source"]})

    def test_graines_t_al_1(self):
        """Trois chaînes ASCII ; sha256 par `echo -n … | sha256sum`, 8 premiers octets en décimal par `bc`. Mutations
        M-AL-1 (8 derniers octets), M-AL-2 (séparateur omis), M-1-05 (graine de règle sur une autre chaîne)."""
        self.assertEqual(aleas.chaine(A, "N1", 0, "sources", 0), "SHOGEN-SIM-BIS|20261004|N1|0|sources|0")
        self.assertEqual(aleas.graine_flux(A, "N1", 0, "sources", 0), 4601104634383262048)
        self.assertEqual(aleas.graine_flux(A, "P-cible", 9999, "observateurs", 3), 1626099482800803730)
        self.assertEqual(aleas.graine_regle(A, "N3", 17),
                         "b99879d412f23f387c9482222ae8f6b1342cb5695ab05d53111d771d359b1059")

    def test_flux_seule_methode_random(self):
        """Le flux est la méthode random() liée d'un random.Random semé par la graine (E-S-42). Mutation M-AL-4 :
        uniform(0, 1) au lieu de random(), de mêmes valeurs (uniform rend a + (b − a)·random()), vue par la forme."""
        u, r = aleas.flux(A, "N1", 0, "sources", 0), random.Random(4601104634383262048)
        self.assertEqual((u.__name__, type(u.__self__)), ("random", random.Random))
        self.assertEqual([u() for _ in range(3)], [r.random() for _ in range(3)])

    def test_champs_refuses(self):
        """« | », non-ASCII, vide, booléen, négatif : ALEAS/champ. Mutations M-1-06 (« | » admis), M-1-07 (non-ASCII
        admis), M-1-08 (booléen admis comme entier)."""
        for cellule, i in (("a|b", 0), ("é", 0), ("", 0), ("N1", True), ("N1", -1), ("N1", "0")):
            self.refus("ALEAS/champ", aleas.chaine, A, cellule, i)

    def test_seuil_plus_petit_flottant(self):
        """seuil(x) ≥ x et le flottant précédent < x, x exact ; 1/3 s'arrondit sous 1/3 au plus proche. Mutation
        M-1-09 : pas vers le haut omis."""
        for x in (Fraction(1, 3), Fraction(1, 700), Fraction(301, 332), Fraction(1, 2 ** 60), 1 - Fraction(1, 2 ** 60)):
            s = aleas.seuil(x)
            self.assertTrue(Fraction(s) >= x > Fraction(math.nextafter(s, 0.0)), x)
        self.assertEqual([aleas.seuil(Fraction(x)) for x in (0, 1, "3/4")], [0.0, 1.0, 0.75])
        for x in (Fraction(-1, 2), Fraction(3, 2), 0.5):
            self.refus("ALEAS/seuil", aleas.seuil, x)

    def test_bernoulli(self):
        """p = 1/3 : vrai juste sous seuil(1/3), faux au seuil ; p = 0 jamais, p = 1 toujours. Mutation M-1-18 : « ≤ »
        au lieu de « < »."""
        s = aleas.seuil(Fraction(1, 3))
        self.assertEqual([aleas.bernoulli(suite(x), s) for x in (0.0, math.nextafter(s, 0.0), s, 0.5)],
                         [True, True, False, False])
        self.assertEqual([aleas.bernoulli(suite(0.0), aleas.seuil(Fraction(0))),
                          aleas.bernoulli(suite(math.nextafter(1.0, 0.0)), aleas.seuil(Fraction(1)))], [False, True])

    def test_empirique_t_al_2(self):
        """EP l.14 (longueurs 1, 2, 3, 5 ; nombres 301, 24, 6, 1) : seuils cumulés 301/332, 325/332, 331/332 ; u au
        seuil exact et juste dessous. Mutations M-1-10 (bisect_left), M-1-11 (seuils non cumulés)."""
        e = aleas.Empirique([(1, 301), (2, 24), (3, 6), (5, 1)])
        cumuls = (Fraction(301, 332), Fraction(325, 332), Fraction(331, 332))
        for s, c in zip(e.seuils, cumuls, strict=True):
            self.assertTrue(Fraction(s) >= c > Fraction(math.nextafter(s, 0.0)), c)
        bas = [math.nextafter(s, 0.0) for s in e.seuils]
        self.assertEqual([e.tirer(suite(x)) for x in (0.0, bas[0], e.seuils[0], bas[1], e.seuils[1], e.seuils[2],
                                                      math.nextafter(1.0, 0.0))], [1, 1, 2, 2, 3, 5, 5])
        for h in ([], [(1, 0)], [(1, -2)], [(1, True)]):
            self.refus("ALEAS/empirique", aleas.Empirique, h)

    def test_geometrique_t_al_2(self):
        """p = 1/700 : seuil de rang k caractérisé contre 1 − (699/700)^k en Fraction, aux rangs 1, 10, 100. Mutation
        M-AL-3 : seuil décalé d'un rang."""
        g = aleas.Geometrique(Fraction(1, 700), A["rangs"], A["garde"])
        self.assertEqual(g.m, 4096)
        for k in (1, 10, 100):
            c = 1 - Fraction(699, 700) ** k
            self.assertTrue(Fraction(g.seuils[k - 1]) >= c > Fraction(math.nextafter(g.seuils[k - 1], 0.0)), k)

    def test_geometrique_frontieres_et_memoire(self):
        """p = 1/4, deux rangs : seuils exacts 1/4 et 7/16 ; au-delà du rang 2, L = 2 + L′ (sans mémoire) ; borne :
        None au-delà ; table arrêtée au premier seuil égal à 1. Mutations M-1-12 (reprise à m − 1), M-1-13 (borne
        exclue), M-1-14 (p = 0 admis), M-1-19 (rang décalé au tirage), M-1-21 (rangs non contrôlés), M-1-22 (table non
        arrêtée à 1)."""
        g = aleas.Geometrique(Fraction(1, 4), 2, 64)
        self.assertEqual(g.seuils, [0.25, 0.4375])
        self.assertEqual([g.tirer(suite(x), 10) for x in (0.0, math.nextafter(0.25, 0.0), 0.25, 0.4374)], [1, 1, 2, 2])
        self.assertEqual([g.tirer(suite(0.5, 0.1), b) for b in (2, 3, 10)], [None, 3, 3])
        self.assertEqual(g.tirer(suite(0.9, 0.9, 0.9, 0.3), 10), 8)
        self.assertEqual(aleas.Geometrique(Fraction(1), 4096, 64).tirer(suite(math.nextafter(1.0, 0.0)), 5), 1)
        self.assertEqual(aleas.Geometrique(Fraction(1, 2), 4096, 64).m, 54)   # 1 − 2^-54 : premier seuil égal à 1
        for p, rangs in ((Fraction(0), 4), (Fraction(5, 4), 4), (0.5, 4), (Fraction(1, 2), 0)):
            self.refus("ALEAS/geometrique", aleas.Geometrique, p, rangs, 64)

    def test_encadrement_ambigu(self):
        """Sans bits de garde, l'encadrement de (2/3)^1 sur 2^-53 laisse deux seuils : refus nommé, jamais un seuil
        deviné. Mutation M-1-15 : borne haute arrondie par défaut (encadrement nul)."""
        self.refus("ALEAS/seuil-ambigu", aleas.Geometrique, Fraction(1, 3), 4, 0)

    def test_flux_a_moitie_renseigne(self):
        """C-4 (a) de la G2 (E-S-41) : composant sans indice, ou indice sans composant : ALEAS/champ, jamais une chaîne
        de quatre champs. Mutation R-03 : « and » au lieu de « or »."""
        for composant, indice in (("sources", None), (None, 0)):
            self.refus("ALEAS/champ", aleas.chaine, A, "N1", 0, composant, indice)

    def test_flux_exige_composant_et_indice(self):
        """C-4 (b) de la G2 (E-S-41) : un flux exige composant et indice ; sans eux, sa chaîne serait celle de la
        graine de règle, et graine_flux(A, "N1", 0, None, None) les 64 premiers bits de graine_regle(A, "N1", 0)
        (12389947756047311666 = 0xabf1efd6e0d92332, par `sha256sum` et `bc`) : ALEAS/champ, pour graine_flux et flux."""
        for composant, indice in ((None, None), ("sources", None), (None, 0)):
            self.refus("ALEAS/champ", aleas.graine_flux, A, "N1", 0, composant, indice)
        self.refus("ALEAS/champ", aleas.flux, A, "N1", 0, None, None)

    def test_geometrique_un_appel_par_tranche(self):
        """C-5 de la G2 (R-02) : p = 1/4, deux rangs, borne 2 (fin de la première tranche) : u() = 0,5 ≥ 7/16 rend
        None après un seul appel de u() (suite(0.5) à une valeur). Mutation R-02 : « base <= borne », tirage de trop."""
        g = aleas.Geometrique(Fraction(1, 4), 2, 64)
        try:
            self.assertIsNone(g.tirer(suite(0.5), 2))
        except StopIteration:
            self.fail("second appel de u() au-delà de la borne")
