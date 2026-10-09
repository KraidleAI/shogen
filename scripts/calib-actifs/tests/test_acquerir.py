"""Acquisition (CA-1, CA-2 ; E-CA-13) contre le serveur local de fichiers synthétiques (aucun réseau) : lecture d'une
URL (essais, pauses, plages), manifeste et reprise. Sommes de référence par sha256sum. Chaque test nomme la mutation
qui le rougit."""
import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest

import acquerir
import socle
from tests.serveur import Serveur

P = socle.lire()


def local(test, base):
    """parametres du lot, pauses notées au lieu d'attendre ; rend (prm, dossier des bruts, pauses notées)."""
    prm = socle.json.loads(socle.json.dumps(P))
    prm["reseau"].update(essais=2, pause_s=7, delai_s=5)
    d, pauses = tempfile.mkdtemp(prefix="ca_acq_"), []
    test.addCleanup(shutil.rmtree, d, True)
    dormir, acquerir.DORMIR = acquerir.DORMIR, pauses.append
    test.addCleanup(setattr, acquerir, "DORMIR", dormir)
    return prm, d, pauses


class TestAcquerir(unittest.TestCase):
    def test_lire_url(self):
        """Une réponse 500 puis le corps : une pause de 7 s, deux requêtes ; plage (2, 4) : octets 2 à 4 (206) ;
        fichier absent (404) : deux essais puis CA/acquisition nommé par le type de l'erreur. Mutations : aucun nouvel
        essai ; pause non faite ; plage ignorée."""
        with Serveur({"/a": b"0123456789"}, pannes={"/a": 1}) as s:
            prm, _d, pauses = local(self, s.base)
            self.assertEqual((acquerir.lire_url(prm, s.base + "/a"), pauses, s.vus), (b"0123456789", [7], ["/a"] * 2))
            self.assertEqual(acquerir.lire_url(prm, s.base + "/a", (2, 4)), b"234")
            with self.assertRaises(socle.Refus) as r:
                acquerir.lire_url(prm, s.base + "/z")
        self.assertEqual((r.exception.code, s.vus[3:], "(HTTPError)" in str(r.exception)),
                         ("CA/acquisition", ["/z", "/z"], True))

    def test_manifeste_reprise(self):
        """Ajout : fichier écrit (sans .partiel restant), ligne URL, date, taille, sha256 (égal à sha256sum), chemin ;
        relu par un manifeste neuf : présent ; fichier altéré : absent ; manifeste sans l'étiquette : CA/acquisition.
        Mutations : reprise sans contrôle du sha256 ; taille fausse ; étiquette non exigée."""
        _prm, d, _p = local(self, "http://127.0.0.1:9")
        m = acquerir.Manifeste(d)
        m.ajouter("u", os.path.join("principale", "kraken", "ETH", "f.csv"), b"abc")
        p = os.path.join(d, "principale", "kraken", "ETH", "f.csv")
        ref = subprocess.run(["sha256sum", p], capture_output=True, text=True).stdout.split(" ")[0]
        with open(os.path.join(d, "manifeste.tsv"), encoding="utf-8") as f:
            lignes = f.read().split(socle.NL)
        champs = lignes[1].split(chr(9))
        self.assertEqual((lignes[0], champs[0], champs[2:], len(champs[1])), (
            socle.ETIQUETTE, "u", ["3", ref, "principale/kraken/ETH/f.csv"], len("2026-10-09T00:00:00Z")))
        self.assertEqual((sorted(os.listdir(os.path.dirname(p))), hashlib.sha256(b"abc").hexdigest()), (["f.csv"], ref))
        self.assertTrue(acquerir.Manifeste(d).present("principale/kraken/ETH/f.csv"))
        with open(p, "wb") as f:
            f.write(b"abd")
        self.assertFalse(acquerir.Manifeste(d).present("principale/kraken/ETH/f.csv"))
        with open(os.path.join(d, "manifeste.tsv"), "w", encoding="utf-8") as f:
            f.write("autre" + socle.NL)
        with self.assertRaises(socle.Refus) as r:
            acquerir.Manifeste(d)
        self.assertEqual(r.exception.code, "CA/acquisition")


if __name__ == "__main__":
    unittest.main()
