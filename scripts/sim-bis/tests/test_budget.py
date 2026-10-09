"""Budget mesuré (SB-11t ; E-S-46 ; adjudication 6 du G0 ; SHOGEN-SIM-BIS-C1-COUT-1) : horloge simulée, attendus
écrits à la main ; chaque test nomme les mutations qui le rougissent."""
import unittest
from unittest import mock

import commun
import executer


class TestBudget(unittest.TestCase):
    def test_chronometrer(self):
        """Deux tâches, horloge simulée 0, 5, 10, 22 ns : résultats dans l'ordre, durées 5 et 12 ns (entiers) ; la
        fonction est appelée entre les deux lectures de l'horloge. Mutations M-11T-01 (durée depuis la première
        lecture), M-11T-02 (une seule lecture par tâche), M-11T-03 (tâches dans le désordre)."""
        vus = []

        def f(x):
            vus.append(x)
            return 2 * x
        with mock.patch.object(executer.time, "perf_counter_ns", side_effect=[0, 5, 10, 22]):
            self.assertEqual(executer.chronometrer(f, [(1,), (3,)]), ([2, 6], [5, 12]))
        self.assertEqual(vus, [1, 3])

    def test_budget(self):
        """Durées 5, 12 puis 7 ns (le maximum ni premier ni dernier : C-10 du contre-contrôle de SB-11), R = 10, deux
        processus, borne 30 ns : coût retenu = le maximum mesuré, 12 ; total 24, trois mesures ; lots de ⌊30/12⌋·2 = 4
        réplications, deux tours de 12 ns chacun, 24 ≤ 30 (C-1 de la G2 de SB-11) : (0, 4), (4, 8), (8, 10) ; durée
        estimée ⌈10·12/2⌉ = 60 ns ; aucune durée : EXEC/budget. Mutations M-11T-04 (moyenne au lieu du maximum, 8),
        M-11T-05 (processus ignorés dans la durée), M-11T-06 (borne par défaut), M-11T-07 (aucune mesure admise),
        G-22 (dernière durée, 7), M-CC-08 (première durée, 5), M-11V-01 (⌊borne·processus/ns⌋), M-11V-03 (processus
        ignorés dans le plan)."""
        self.assertEqual(executer.budget([5, 12, 7], 10, 2, 30), {"ns_max": 12, "ns_total": 24, "mesures": 3,
                                                                  "plages": [(0, 4), (4, 8), (8, 10)], "duree_ns": 60})
        self.assertEqual(executer.budget([7], 3, 2, 30)["duree_ns"], 11)
        with self.assertRaises(commun.Refus) as r:
            executer.budget([], 10, 2, 30)
        self.assertEqual(r.exception.code, "EXEC/budget")


if __name__ == "__main__":
    unittest.main()
