"""Aléas SB-1 (E-S-41, E-S-42 ; T-AL-1) : graines par `sha256sum` et `bc` (8 premiers octets en décimal) ; chaque test
nomme les mutations qui le rougissent."""
import random
import unittest

import aleas
import commun

A = commun.charger_parametres(environ={})["aleas"]


class TestAleas(unittest.TestCase):
    def refus(self, code, f, *a):
        with self.assertRaises(commun.Refus) as c:
            f(*a)
        self.assertEqual(c.exception.code, code)

    def test_parametres(self):
        """GRAINE fixée par le G0 (E-S-41) et préfixe, de parametres.json."""
        self.assertEqual(A, {"prefixe": "SHOGEN-SIM-BIS", "graine": 20261004, "source": A["source"]})

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

