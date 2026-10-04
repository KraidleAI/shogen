"""SHOGEN-POOLEE-BLOC-1 (a) : plancher d'erreur-type par blocs de la strate poolée, valeurs à la main sur une sortie r1
réduite ; chaque test nomme la mutation qui le rougit."""
import unittest
from decimal import Decimal

import poolee_bloc


def strate(n, k, p, s2, zb=Decimal(1)):
    return {"n": n, "K": k, "P_more": Decimal(p), "bloc": {"sigma2_bloc": Decimal(s2), "z_bloc": zb}}


class TestPooleeBloc(unittest.TestCase):
    def test_a_la_main(self):
        """(10 − 100·0,05) + (12 − 200·0,04) = 5 + 4 = 9 ; σ̂² 4 + 5 = 9 ; z = 9/√9 = 3. Rougit si : racine oubliée ;
        numérateur ou variance d'une seule strate."""
        base = {"strates": {"calme": strate(100, 10, "0.05", "4"), "stress": strate(200, 12, "0.04", "5")},
                "poolee": {"z_pool": Decimal(1), "motif": None}}
        r = poolee_bloc.poolee_bloc(base)
        self.assertEqual((r["numerateur"], r["variance"], r["z"], r["motif"]), (9, 9, 3, None))

    def test_motifs_de_non_publication(self):
        """Rougit si z_pool,bloc est publié malgré un z_bloc de strate non publié ou une strate poolée sans z_pool."""
        base = {"strates": {"calme": strate(100, 10, "0.05", "4"), "stress": strate(200, 12, "0.04", "5", None)},
                "poolee": {"z_pool": Decimal(1), "motif": None}}
        self.assertEqual(poolee_bloc.poolee_bloc(base)["z"], None)
        self.assertIn("stress", poolee_bloc.poolee_bloc(base)["motif"])
        base["strates"]["stress"]["bloc"]["z_bloc"] = Decimal(1)
        base["poolee"] = {"z_pool": None, "motif": "une seule strate"}
        self.assertEqual(poolee_bloc.poolee_bloc(base)["z"], None)
        self.assertIn("une seule strate", poolee_bloc.poolee_bloc(base)["motif"])

    def test_ligne_par_strate_a_precision_50(self):
        """Constat de l'exécution (journal G1 §3) : le terme K_s − n_s·P̂_more,s imprimé par strate l'était au contexte
        par défaut (28 chiffres). 1 − 3·0,3…3 (50 chiffres) = 1E-50 au contexte nommé, 0 à 28 chiffres. Rougit si le
        terme par strate n'est pas calculé sous r1.contexte_decimal()."""
        base = {"strates": {"calme": strate(3, 1, "0." + "3" * 50, "4"), "stress": strate(100, 10, "0.05", "4")},
                "poolee": {"z_pool": Decimal(1), "motif": None}}
        self.assertIn("K_s − n_s·P̂_more,s = 1E-50 ;", poolee_bloc.poolee_bloc(base)["lignes"][1])


if __name__ == "__main__":
    unittest.main()
