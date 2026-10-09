"""Bruts synthétiques aux six formats relus par bougies.charger ; lignes de valeurs et fenêtre descriptive de septembre
(E-CA-20, E-CA-22 ; PROPOSITION §4.1). Chaque test nomme la mutation qui le rougit."""
import os
import shutil
import tempfile
import unittest

import bougies
import socle
import tau
from tests import synthetiques as sy

P = socle.lire()
DESC = {"debut": 1788566100, "fin": 1788566700, "sans": ["kraken"], "source": ""}     # 2026-09-04 23:55 à 09-05 00:05


class TestEcriture(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="ca_ecr_")
        self.addCleanup(shutil.rmtree, self.d, True)

    def test_aller_retour(self):
        """Chaque (actif, place) de la lecture A écrit au format de sa place puis relu par bougies.charger : minutes
        actives égales à la série synthétique ; fenêtre descriptive : kraken absent. Mutation : format d'une place
        confondu avec un autre (écrivain ou lecteur)."""
        sy.ecrire_bruts(P, self.d, "principale")
        for a in socle.ACTIFS:
            for p, s in sy.series(P, a).items():
                r = bougies.charger(P, self.d, "principale", p, a, sy.FEN)
                self.assertEqual({t: v for t, v in r.items() if v[1]}, {t: v for t, v in s.items() if v[1]}, (a, p))
        q = dict(P, fenetre_descriptive=DESC)
        sy.ecrire_bruts(q, self.d, "descriptive", DESC)
        self.assertEqual(sorted(os.listdir(os.path.join(self.d, "descriptive"))),
                         ["binance", "bitfinex", "bitstamp", "coinbase", "okx"])

    def test_corps_et_septembre(self):
        """Lignes de valeurs : cinq par actif, τ des places du résultat ; septembre : ETH et USDT calculés sans kraken,
        USDC refusé (trois places, sous N_min = 4 : CA/population), refus imprimé, jamais levé. Mutations : kraken
        gardé en septembre ; refus de septembre levé."""
        res = {a: tau.calcul_actif(P, a, sy.series(P, a), sy.FEN, sy.BTC) for a in socle.ACTIFS}
        lignes = tau.corps(P, res)
        self.assertEqual(len(lignes), 15)
        self.assertIn(f"[USDT] τ des places {res['USDT']['places']['tau']} ;", lignes[12])
        q = dict(P, fenetre_descriptive=DESC)
        sy.ecrire_bruts(q, self.d, "descriptive", DESC)
        sep = tau.septembre(q, self.d, sy.BTC)
        self.assertEqual([x.split(" : ")[1][:19] for x in sep[1:2]] + [x.split(" : ")[1][:12] for x in sep[0::2]],
                         ["REFUS CA/population", "τ des places", "τ des places"])


if __name__ == "__main__":
    unittest.main()
