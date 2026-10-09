"""Descriptifs (E-CA-20 ; PROPOSITION §4.3 pt 5, §4.4, §4.6 ; AVIS Q-CA-04, Q-CA-06, Q-CA-07) : jamais décisifs, le
fragment ne change d'aucun octet quand ils sont calculés ; queue par place sur des écarts écrits à la main. Chaque test
nomme la mutation qui le rougit."""
import json
import unittest
from decimal import Decimal
from fractions import Fraction as F

import socle
import tau
from tests import synthetiques as sy

P = socle.lire()


class TestDescriptifs(unittest.TestCase):
    def test_fragment_inchange(self):
        """E-CA-20 : fragment des trois actifs identique à l'octet avant et après le calcul des descriptifs ; lignes à
        l'actif, troisième terme sur toutes les places horodatées d'ETH (bitstamp, coinbase, okx). Mutation : un
        descriptif qui écrit dans les résultats."""
        res = {a: tau.calcul_actif(P, a, sy.series(P, a), sy.FEN, sy.BTC) for a in socle.ACTIFS}
        avant = json.dumps(tau.fragment(P, res), sort_keys=True)
        lignes = [x for a in socle.ACTIFS for x in tau.descriptifs(P, a, res[a])]
        self.assertEqual(json.dumps(tau.fragment(P, res), sort_keys=True), avant)
        self.assertIn("[ETH] descriptif : troisième terme sur toutes les places horodatées (bitstamp, coinbase, okx)",
                      lignes[0])
        self.assertTrue(all(x.split(" descriptif : ")[0] in ("[ETH]", "[USDC]", "[USDT]") for x in lignes))

    def test_queue(self):
        """Calme : 999 écarts de 0,01, un de 0,05 (okx), un de 0,09 (bitstamp, âge 3) : P99,9 au rang 1 000 = 0,05,
        queue = 0,09 ; stress : 2 996 de 0,01, puis 0,02, 0,03, 0,04, 0,05 (okx, âges 5, 9, 20 pour les trois
        derniers) : P99,9 au rang 2 997 = 0,02 ; par place : bitstamp (1 cellule, part 1/4, âge médian 3), okx (3, 3/4,
        âge médian au rang 2 = 9) ; variante « minutes actives seules » : clôtures d'âge 0 seules. Mutations : queue à
        « ≥ P99,9 » ; part rapportée aux cellules de la place ; âge maximal au lieu du médian ; masque retiré."""
        cel = {"calme": ([F(1, 100)] * 999 + [F(5, 100), F(9, 100)], ["kraken"] * 999 + ["okx", "bitstamp"],
                         [0] * 999 + [1, 3]),
               "stress": ([F(1, 100)] * 2996 + [F(2, 100), F(3, 100), F(4, 100), F(5, 100)],
                          ["kraken"] * 2997 + ["okx"] * 3, [0] * 2997 + [5, 9, 20])}
        self.assertEqual(tau.queue(P, cel), {"bitstamp": (1, F(1, 4), 3), "okx": (3, F(3, 4), 9)})
        r = {"closes": {"kraken": [F(10), F(10), F(11), None]}, "ages": {"kraken": [0, 1, 0, None]}}
        self.assertEqual(tau.actives_seules(r), {"kraken": [F(10), None, F(11), None]})

    def test_affiche_et_planchers_seuls(self):
        """Impression à 10⁻¹⁰ : 1/3, 0,0055, None ; mode « planchers seuls » (USDT) : ni variante ni queue, la ligne des
        agrégateurs gardée. Mutation : variante calculée sans population."""
        self.assertEqual([tau.affiche(x) for x in (F(1, 3), Decimal("0.0055"), None)],
                         ["0.3333333333", "0.0055000000", "-"])
        q = json.loads(json.dumps(P))
        q["lectures"]["A"]["modes"]["USDT"] = "planchers_seuls"
        lignes = tau.descriptifs(q, "USDT", tau.calcul_actif(q, "USDT", sy.series(q, "USDT"), sy.FEN, sy.BTC))
        self.assertEqual([x.split(" : ")[1][:15] for x in lignes], ["troisième terme", "τ des agrégateu"])


if __name__ == "__main__":
    unittest.main()
