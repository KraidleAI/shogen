"""Complétude imprimée (SHOGEN-CALIB-FORMES-API-1 ; DECISION pt 5 ; lot DETTES-T2) : minutes reçues sur attendues
dans calib_actifs.txt, par tau.main sur le banc de test_cli."""
import os
import tempfile
import unittest

import socle
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
        imprimées ; place ou fenêtre mal nommée. C-13 : Coinbase et Bitstamp, seconde couverture de 2 pages (début − h
        et début + h, h = 74 et 249 minutes) ; mutation : second découpage non compté. R-5 du contre-contrôle cc2 :
        dossier de Coinbase écrit à la main (une page, une page du second découpage redemandée en demi-pages, une
        autre non) : pages redemandées 1, seconde couverture 2 pages ; mutation : demi-pages du second découpage
        comptées comme pages."""
        argv, d = banc(self)

        def sortie():
            tau.main(argv, {})
            return lire(d)[0]
        texte = essai(sortie)
        lignes = [x for x in texte if "minutes reçues sur attendues" in x] if isinstance(texte, list) else [texte]
        tete = "descriptif : minutes reçues sur attendues, "
        self.assertEqual([lignes[i] for i in (3, 9, 17, 18)] if len(lignes) == 29 else lignes, [
            f"[ETH] {tete}coinbase (principale) : total 8/10 ; pages redemandées 0 ; seconde couverture 2 pages ; par "
            "page 1775260500 8/10",
            f"[USDC] {tete}kraken (principale) : total 8/10",
            f"[ETH] {tete}bitfinex (descriptive) : total 8/10 ; pages redemandées 0 ; par page 1788566100 8/10",
            f"[ETH] {tete}bitstamp (descriptive) : total 10/10 ; pages redemandées 0 ; seconde couverture 2 pages ; "
            "par page 1788566100 10/10"])
        b = tempfile.mkdtemp(dir=d)
        os.makedirs(os.path.join(b, "principale", "coinbase", "ETH"))
        for nom in ("page-0.json", "double-1.json", "double-1.1.json", "double-1.2.json", "double-2.json"):
            open(os.path.join(b, "principale", "coinbase", "ETH", nom), "w", encoding="ascii").close()
        f = {"debut": 1775001600, "fin": 1775002200}
        self.assertEqual(tau.completude(socle.lire(), "ETH", "principale", f, {"coinbase": {}}, b), [
            f"[ETH] {tete}coinbase (principale) : total 0/10 ; pages redemandées 1 ; seconde couverture 2 pages ; par "
            "page 1775001600 0/10"])


if __name__ == "__main__":
    unittest.main()
