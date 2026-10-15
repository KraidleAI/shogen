"""Complétude imprimée (SHOGEN-CALIB-FORMES-API-1 ; DECISION pt 5 ; lot DETTES-T2) : minutes reçues sur attendues
dans calib_actifs.txt, par tau.main sur le banc de test_cli."""
import unittest

import tau
from tests.test_cli import banc, lire
from tests.test_formes import essai


class TestComptes(unittest.TestCase):
    def test_comptes_imprimes(self):
        """DECISION pt 5 : dans calib_actifs.txt, après septembre, une ligne par (actif, place) et par fenêtre
        (principale, puis descriptive sans kraken) : 16 + 13 lignes, minutes reçues sur attendues, au total et par page
        pour les places paginées. Fenêtres synthétiques de 10 minutes (une page) ; comptes à la main depuis la règle de
        tests/synthetiques.py (minute i inactive si (i + j) % 5 == 0 et i > 0 ; Coinbase, Bitfinex et Kraken n'écrivent
        pas les minutes sans échange) : coinbase d'ETH (j = 3) et kraken d'USDC (j = 3) 8 sur 10, bitfinex (j = 1) 8,
        bitstamp 10. Mutations : lignes omises ; fenêtre descriptive omise ; total, reçues ou attendues faux ; pages non
        imprimées ; place ou fenêtre mal nommée."""
        argv, d = banc(self)

        def sortie():
            tau.main(argv, {})
            return lire(d)[0]
        texte = essai(sortie)
        lignes = [x for x in texte if "minutes reçues sur attendues" in x] if isinstance(texte, list) else [texte]
        tete = "descriptif : minutes reçues sur attendues, "
        self.assertEqual([lignes[i] for i in (3, 9, 17, 18)] if len(lignes) == 29 else lignes, [
            f"[ETH] {tete}coinbase (principale) : total 8/10 ; pages redemandées 0 ; par page 1775260500 8/10",
            f"[USDC] {tete}kraken (principale) : total 8/10",
            f"[ETH] {tete}bitfinex (descriptive) : total 8/10 ; pages redemandées 0 ; par page 1788566100 8/10",
            f"[ETH] {tete}bitstamp (descriptive) : total 10/10 ; pages redemandées 0 ; par page 1788566100 10/10"])


if __name__ == "__main__":
    unittest.main()
