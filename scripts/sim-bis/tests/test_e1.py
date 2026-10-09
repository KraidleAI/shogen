"""E1 câblée, SB-11j (E-S-38 ; Q-SI-8 (a), (d) et (e) de SIM-INTEG ; point (6) de l'ajout daté du G0 du 2026-10-05
15:05:43 UTC) : attendus écrits à la main, produits par `bc -l`, ou recalculés ici depuis un seul appel de
calib_fiv.replication ; chaque test nomme les mutations qui le rougissent."""
import functools
import json
import os
import shutil
import tempfile
import unittest
from decimal import Decimal
from fractions import Fraction
from unittest import mock

import calib_fiv
import calibration
import commun
import e1
import executer

PRM = commun.charger_parametres(environ={})
K_ = PRM["calibration"]
EP = calibration.charger(PRM, environ={})["episodes"]
HOTES = [h for h, _f in K_["unites"]]
P = (Fraction(1, 10), Fraction(5), 60)
E1R = dict(PRM, e1=dict(PRM["e1"], phi=[[1, 100], [1, 10]], kappa=[5], tau_D=[60], replications=2,
                        cellule="E1-essai"))


@functools.lru_cache(maxsize=None)
def cal_e1():
    """Calendrier d'E1 (masque mesuré de PLAN-S2BIS-2), lu une fois."""
    return calib_fiv.calendrier_e1(PRM, environ={})


class TestReplicationE1(unittest.TestCase):
    def test_courbes_d_un_seul_appel(self):
        """Q-SI-8 (a) et (e) : réplications 0 et 1 du point (1/10, 5, 60) : un seul appel de calib_fiv.replication
        par réplication ; courbe de I_t et courbes des dix hôtes du format sur le masque de chaque strate, égales aux
        FIV exacts de calib_fiv.courbe des séries rendues par cet appel ; le lot du point (cellule E1-essai-1_10-5-60,
        [0, 2)) porte ces enregistrements. Mutations M-11J-01 (hôtes d'une autre réplication), M-11J-02 (I_t sur les
        positions générées au lieu du masque), M-11J-03 (deux appels), M-11J-04 (courbes sur l ≠ calibration.ell)."""
        cal, ell = cal_e1(), K_["ell"]
        for i in (0, 1):
            with mock.patch.object(calib_fiv, "replication", wraps=calib_fiv.replication) as m:
                r = e1.replication_e1(E1R, EP, cal, P, i)
            self.assertEqual(m.call_count, 1)
            x = calib_fiv.replication(E1R, EP, cal, P, "E1-essai-1_10-5-60", i)
            self.assertEqual(sorted(r["strates"]), sorted(x["strates"]))
            for s, (pos, val) in x["strates"].items():
                self.assertEqual(r["strates"][s]["I"], [c["fiv"] for c in calib_fiv.courbe(pos, val, ell, K_)], s)
                self.assertEqual(sorted(r["strates"][s]["unites"]), sorted(HOTES), s)
                for h, d in x["unites"][s].items():
                    attendu = [c["fiv"] for c in calib_fiv.courbe(pos, d, ell, K_)]
                    self.assertEqual(r["strates"][s]["unites"][h], attendu, (s, h))
            if i == 1:
                d = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
                self.addCleanup(shutil.rmtree, d)
                c, _h = e1.lot_e1(E1R, EP, cal, P, (1, 2), 1, d, ["e"])
                self.assertEqual(os.path.basename(c), "E1-essai-1_10-5-60.000001-000002.lot")
                with open(c, "rb") as f:
                    lot = json.loads(f.read().split(commun.NL.encode(), 1)[1])
                self.assertEqual(lot["enregistrements"], [executer.jsonable(r)])

    def test_moyennes_point(self):
        """Agrégation d'un point (enregistrements relus, chaînes JSON) : I_t = 1, 2 ; 2, 4 ; indéfinie : moyenne exacte
        3/2, 3, une indéfinie ; variance exacte des définies, dénominateur m − 1 : 1/2, 2 ; écart-type par Decimal.sqrt
        sous le contexte de r1 : √(1/2), √2 (bc -l, à 10⁻⁴⁹ près) ; une seule définie : variance et écart-type None.
        Hôtes : a = 1, 2 ; 3, 4 ; 1/2, 1 : 3/2, 7/3, aucune indéfinie ; b défini une fois sur trois : deux indéfinies
        (Q-SI-8 (d)). Mutations M-11J-05 (variance au dénominateur m), M-11J-06 (indéfinies comptées pour 0), M-11J-07
        (racine sous le contexte par défaut)."""
        def r(i, ii, a, b):
            return {"i": i, "strates": {"calme": {"I": ii, "unites": {"a": a, "b": b}}}}
        n = [None, None]
        m = e1.moyennes_point([r(0, ["1", "2"], ["1", "2"], n), r(1, ["2", "4"], ["3", "4"], ["1", "1"]),
                               r(2, n, ["1/2", "1"], n)], K_)["calme"]
        self.assertEqual((m["I"], m["variance"]), ({"fiv": [Fraction(3, 2), 3], "definies": 2, "indefinies": 1},
                                                  [Fraction(1, 2), 2]))
        for x, ref in zip(m["ecart_type"], ("0.707106781186547524400844362104849039284835937688474036588339",
                                            "1.414213562373095048801688724209698078569671875376948073176679")):
            self.assertLess(abs(x - Decimal(ref)), Decimal("1E-49"))
        self.assertEqual(m["unites"], {"a": {"fiv": [Fraction(3, 2), Fraction(7, 3)], "definies": 3, "indefinies": 0},
                                       "b": {"fiv": [1, 1], "definies": 1, "indefinies": 2}})
        m = e1.moyennes_point([r(0, ["1", "2"], ["1", "2"], n), r(1, n, ["1", "2"], n)], K_)["calme"]
        self.assertEqual((m["variance"], m["ecart_type"]), ([None, None], [None, None]))


if __name__ == "__main__":
    unittest.main()
