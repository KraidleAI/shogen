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
        """Durées 5 et 12 ns, R = 10, deux processus, borne 30 ns : coût retenu = le maximum mesuré, 12 ; lots de
        ⌊30·2/12⌋ = 5 réplications : (0, 5), (5, 10) ; durée estimée ⌈10·12/2⌉ = 60 ns ; aucune durée : EXEC/budget.
        Mutations M-11T-04 (moyenne au lieu du maximum), M-11T-05 (processus ignorés dans la durée), M-11T-06 (borne
        par défaut), M-11T-07 (aucune mesure admise)."""
        self.assertEqual(executer.budget([5, 12], 10, 2, 30), {"ns_max": 12, "ns_total": 17, "mesures": 2,
                                                               "plages": [(0, 5), (5, 10)], "duree_ns": 60})
        self.assertEqual(executer.budget([7], 3, 2, 30)["duree_ns"], 11)
        with self.assertRaises(commun.Refus) as r:
            executer.budget([], 10, 2, 30)
        self.assertEqual(r.exception.code, "EXEC/budget")


if __name__ == "__main__":
    unittest.main()
