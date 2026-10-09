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
    prm["series"]["binance"]["url"] = base + "/b/{s}-1m-{m}.zip"
    prm["series"]["okx"]["url"] = base + "/o/{mm}/{s}-{m}.zip"
    prm["reseau"].update(essais=2, pause_s=7, delai_s=5)
    d, pauses = tempfile.mkdtemp(prefix="ca_acq_"), []
    test.addCleanup(shutil.rmtree, d, True)
    dormir, acquerir.DORMIR = acquerir.DORMIR, pauses.append
    test.addCleanup(setattr, acquerir, "DORMIR", dormir)
    return prm, d, pauses


def zips(prefixe, symbole, somme=True, mauvais=()):
    """Trois faux mensuels (2026-04 à 06) et, pour Binance, leurs .CHECKSUM (« sha256  nom »), faux pour `mauvais`."""
    f = {}
    for m in ("2026-04", "2026-05", "2026-06"):
        chemin = f"{prefixe}/{symbole}-1m-{m}.zip" if somme else f"{prefixe}/{m.replace('-', '')}/{symbole}-{m}.zip"
        f[chemin] = f"{symbole} {m}".encode()
        if somme:
            h = hashlib.sha256(f[chemin] + (b"x" if m in mauvais else b"")).hexdigest()
            f[chemin + ".CHECKSUM"] = f"{h}  {symbole}-1m-{m}.zip".encode()
    return f


class TestAcquerir(unittest.TestCase):
    def test_mois(self):
        """Fenêtre principale : 2026-04, 05, 06 ; descriptive : 2026-09 ; 1798758000 (2026-12-31 23:00) à 1798765200
        (2027-01-01 01:00) : 2026-12 et 2027-01. Mutation : passage d'année perdu (mois 13)."""
        self.assertEqual(acquerir.mois(P["fenetre"]), ["2026-04", "2026-05", "2026-06"])
        self.assertEqual(acquerir.mois(P["fenetre_descriptive"]), ["2026-09"])
        self.assertEqual(acquerir.mois({"debut": 1798758000, "fin": 1798765200}), ["2026-12", "2027-01"])

    def test_binance_checksum_et_manifeste(self):
        """Trois mensuels et leurs .CHECKSUM : manifeste à l'étiquette, une ligne par fichier (URL, date, taille,
        sha256 égal à sha256sum du fichier écrit) ; .CHECKSUM faux en mai : CA/acquisition, mai absent du manifeste.
        Mutations : contrôle du .CHECKSUM retiré ; taille ou sha256 faux au manifeste."""
        with Serveur(zips("/b", "ETHUSDT")) as s:
            prm, d, _p = local(self, s.base)
            acquerir.mensuels(prm, acquerir.Manifeste(d), "principale", P["fenetre"], "binance", "ETH")
        with open(os.path.join(d, "manifeste.tsv"), encoding="utf-8") as f:
            lignes = f.read().split(socle.NL)
        self.assertEqual((lignes[0], len(lignes)), (socle.ETIQUETTE, 5))
        url, _date, taille, sha, rel = lignes[2].split(chr(9))
        ref = subprocess.run(["sha256sum", os.path.join(d, rel)], capture_output=True, text=True).stdout.split(" ")[0]
        self.assertEqual((url, taille, sha, rel), (s.base + "/b/ETHUSDT-1m-2026-05.zip", "15", ref,
                                                    "principale/binance/ETH/ETHUSDT-1m-2026-05.zip"))
        with Serveur(zips("/b", "USDCUSD", mauvais=("2026-05",))) as s:
            prm, d, _p = local(self, s.base)
            with self.assertRaises(socle.Refus) as r:
                acquerir.mensuels(prm, acquerir.Manifeste(d), "principale", P["fenetre"], "binance", "USDC")
        self.assertEqual((r.exception.code, len(acquerir.Manifeste(d).vus)), ("CA/acquisition", 1))

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


    def test_okx_reprise(self):
        """OKX : chemin par mois AAAAMM, trois fichiers ; second passage : aucune requête neuve (reprise). Mutations :
        mois AAAAMM perdu ; reprise ignorée."""
        with Serveur(zips("/o", "ETH-USDT", somme=False)) as s:
            prm, d, _p = local(self, s.base)
            for _ in range(2):
                acquerir.mensuels(prm, acquerir.Manifeste(d), "principale", P["fenetre"], "okx", "ETH")
        self.assertEqual(s.vus, [f"/o/2026{m:02d}/ETH-USDT-2026-{m:02d}.zip" for m in (4, 5, 6)])


if __name__ == "__main__":
    unittest.main()
