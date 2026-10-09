"""Socle : variable de campagne, lecture stricte de parametres.json, lecture retenue (E-CA-03, E-CA-06, E-CA-12,
E-CA-24). Attendus écrits à la main (date -u -d pour les instants) ; chaque test nomme la mutation qui le rougit."""
import json
import os
import tempfile
import unittest

import socle


class TestSocle(unittest.TestCase):
    def assertRefus(self, code, f, *a):
        with self.assertRaises(socle.Refus) as r:
            f(*a)
        self.assertEqual(r.exception.code, code)
        return str(r.exception)

    def test_variable(self):
        """T-CA-SOC-2 : environnement passé en argument ; la variable posée, même vide : CA/variable ; absente :
        aucun refus. Mutation M-CA-02 : garde retirée."""
        self.assertRefus("CA/variable", socle.garde, {"SHOGEN_S2_CAMPAGNE_CONTROL": ""})
        self.assertIsNone(socle.garde({"PATH": "/usr/bin"}))

    def test_parametres_lus(self):
        """Fenêtre 1775001600 (2026-04-01) à 1782864000 (2026-07-01) ; lecture A : 6, 4, 6 places, N_min 4, modes
        calibre, dernière transaction coinbase pour ETH et USDT ; A-prime : 4, 3, 4 places ; unités 10, 8, 10.
        Mutation : lecture A-prime retenue (rend 4, 3, 4)."""
        p = socle.lire()
        self.assertIsInstance(p, dict)
        self.assertEqual((p["fenetre"]["debut"], p["fenetre"]["fin"]), (1775001600, 1782864000))
        lec = socle.lecture(p)
        self.assertEqual({a: len(v) for a, v in lec["places"].items()}, {"ETH": 6, "USDC": 4, "USDT": 6})
        self.assertEqual((lec["n_min"], set(lec["modes"].values())), ({"ETH": 4, "USDC": 4, "USDT": 4}, {"calibre"}))
        self.assertEqual(lec["derniere_transaction"], {"ETH": ["coinbase"], "USDC": [], "USDT": ["coinbase"]})
        prime = p["lectures"]["A-prime"]["places"]
        self.assertEqual({a: len(v) for a, v in prime.items()}, {"ETH": 4, "USDC": 3, "USDT": 4})
        self.assertEqual([len(p["unites"][a]) for a in socle.ACTIFS], [10, 8, 10])

    def test_parametres_schema(self):
        """Clé en trop, booléen pour un entier : CA/parametres. Mutations : schéma retiré ; type non contrôlé ; clé en
        trop admise."""
        for modif in (lambda p: p.update(inconnu=1), lambda p: p["passes"].update(A=False)):
            with open(socle.PARAMETRES, encoding="utf-8") as f:
                p = json.load(f)
            modif(p)
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
                json.dump(p, f)
            self.addCleanup(os.remove, f.name)
            self.assertRefus("CA/parametres", socle.lire, f.name)


if __name__ == "__main__":
    unittest.main()
