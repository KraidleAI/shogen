"""INT-P2-16 (Q-5 adjugée le 2026-10-17 ; AVIS Q-C-05 l.94 ; E-C-37, E-C-40) : capture des octets, sur fixtures, sans
réseau (`lire` et `pause` remplacés). Noms des fichiers et lignes du manifeste écrits à la main ; sha256 des fixtures
relevés par `sha256sum` hors du code ; formes et fixtures de `test_smoke`."""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

from shogen_s2bis.collecte import capture, decodeurs, entree
from shogen_s2bis.collecte.lecture import Lecture
from tests.test_entree import configurations
from tests.test_secondaire import carte, fichiers
from tests.test_smoke import CARTE, PIECES, POOL, forme, lire

SHA = {"binance_btc": "880903276bc688eecfb02e8b5e30f60c6a195dda6c372bce445063f8621f61f5",
       "binance_usdc": "17397032db28cad708617e8a1ee480dfa6a27ed10cb35a993bc0a7411d1bb5cc",
       "okx_usdc_usdt": "78044f24a858eb887fc0b38f124ddaf4c9ad3f5be624ef0876165854042b3ae8",
       "curve_usdc_usdt": "82566c09417ff6d00d0ec28cfbe66f1a23c24b7933ff87742b43c8ea11613a99",
       "kraken_eth": "23a9650b0891b949dbba34c48fa869b0a4147955182df34f610849a2d59ce3a5"}
VIDE = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
FORMES = ("binance_btc", "okx_usdc_usdt", "binance_usdc", "curve_usdc_usdt")


class Capture(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.d, self.appels, self.vus = d.name, [], []

    def faux(self, servies):
        def lire_faux(req, suivi, delai, tls):
            self.appels.append((req.hote, req.chemin, delai))
            self.vus.append((req.port, tls is capture.http.CONTEXTE))
            dec = req.chemin[1:]
            return servies.get(dec, Lecture("ok", 1_000 + len(self.appels), 9_000, code=200, octets=lire(PIECES[dec])))
        return lire_faux

    def capturer(self, **servies):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = capture.capturer([forme(d) for d in FORMES], [{**forme("kraken_eth"), "port": 8443}], (POOL, CARTE),
                                    self.d, lire=self.faux(servies), pause=lambda s: self.appels.append(("pause", s)))
        return code, out.getvalue(), err.getvalue()

    def lu(self, nom):                                                # None : fichier absent
        if os.path.exists(os.path.join(self.d, nom)):
            with open(os.path.join(self.d, nom), "rb") as f:
                return f.read()

    def test_octets_ecrits_et_manifeste_rien_sur_la_sortie(self):
        """Octets bruts de chaque forme dans `<rôle>-<forme>.bin`, égaux à la fixture servie ; manifeste : fichier,
        sha256, statut, code, départ ; aucune ligne imprimée (garde : les fichiers portent les prix décodables) ; port
        de chaque forme (8443 pour la carte) et contexte TLS transmis (C-2 de la G2 de la série)."""
        code, out, err = self.capturer()
        noms = ["pool-binance-btc.bin", "temoin-okx-usdc-usdt.bin", "pool-binance-usdc.bin",
                "temoin-curve-usdc-usdt.bin", "carte-kraken-eth.bin"]
        self.assertEqual((code, out, err, sorted(os.listdir(self.d))), (0, "", "", sorted(noms + ["captures.txt"])))
        self.assertEqual([self.lu(n) for n in noms], [lire(PIECES[d]) for d in FORMES + ("kraken_eth",)])
        self.assertEqual((self.lu("captures.txt") or b"").decode().splitlines(), [
            f"pool-binance-btc.bin {SHA['binance_btc']} ok 200 1001",
            f"temoin-okx-usdc-usdt.bin {SHA['okx_usdc_usdt']} ok 200 1002",
            f"pool-binance-usdc.bin {SHA['binance_usdc']} ok 200 1004",
            f"temoin-curve-usdc-usdt.bin {SHA['curve_usdc_usdt']} ok 200 1005",
            f"carte-kraken-eth.bin {SHA['kraken_eth']} ok 200 1006"])
        self.assertEqual(decodeurs.decoder("okx_usdc_usdt", self.lu("temoin-okx-usdc-usdt.bin"))[1][0]["prix"],
                         "1.00062")
        self.assertEqual(self.appels, [
            ("api.binance.com", "/binance_btc", POOL), ("www.okx.com", "/okx_usdc_usdt", POOL), ("pause", 1),
            ("api.binance.com", "/binance_usdc", POOL), ("rpc.mevblocker.io", "/curve_usdc_usdt", POOL),
            ("api.kraken.com", "/kraken_eth", CARTE)])
        self.assertEqual(self.vus, [(443, True)] * 4 + [(8443, True)])

    def test_code_1_si_le_pool_ou_le_temoin_echoue_carte_declaree(self):
        """Témoin en panne de transport : 1, fichier vide écrit et déclaré ; carte seule en panne : 0, déclarée."""
        delai = Lecture("panne_transport", 7, 10_000_007, sous_type="delai")
        code, out, _e = self.capturer(okx_usdc_usdt=delai, kraken_eth=Lecture("panne_http", 8, 9, code=451))
        lignes = (self.lu("captures.txt") or b"").decode().splitlines()
        self.assertEqual((code, out, self.lu("temoin-okx-usdc-usdt.bin"), lignes[1:2] + lignes[4:5]), (
            1, "", b"", [f"temoin-okx-usdc-usdt.bin {VIDE} panne_transport - 7",
                         f"carte-kraken-eth.bin {VIDE} panne_http 451 8"]))
        self.setUp()
        self.assertEqual(self.capturer(kraken_eth=Lecture("panne_http", 8, 9, code=451))[0], 0)

    def test_refus_avant_toute_lecture(self):
        """Dossier absent, nom de forme hors de NOM, fichier ou manifeste déjà présent (jamais écrasé) : refus nommé,
        avant toute lecture, aucun fichier écrit."""
        with open(os.path.join(self.d, "pool-binance-btc.bin"), "wb") as f:
            f.write(b"avant")
        open(os.path.join(self.d, "captures.txt"), "w").close()
        cas = [(os.path.join(self.d, "absent"), [forme(d) for d in FORMES], "dossier"),
               (self.d, [forme(d) for d in FORMES], "fichier"), (self.d, [forme("kraken_eth")], "fichier")]
        cas += [(self.d, [{**forme("kraken_eth"), "nom": n}], "nom") for n in ("../x", ".x", "A", "")]
        for dossier, formes, motif in cas:
            with self.subTest(motif=motif, nom=formes[0]["nom"]):
                with self.assertRaises(capture.CaptureRefusee) as e:
                    capture.capturer(formes, [], (POOL, CARTE), dossier, lire=self.faux({}))
                self.assertEqual(str(e.exception).split(" : ")[0], motif)
        self.assertEqual((self.appels, self.lu("pool-binance-btc.bin"), sorted(os.listdir(self.d))),
                         ([], b"avant", ["captures.txt", "pool-binance-btc.bin"]))

    def test_jamais_ecrase_apres_le_controle(self):              # C-1 de la G2 de la série INT-P2
        """Un fichier apparu après le contrôle des noms (pendant la lecture précédente) n'est jamais écrasé, octets
        ni manifeste (ouverture exclusive) : FileExistsError, ses octets gardés (le contrôle seul laisse une course)."""
        for cible, pendant in (("pool-binance-usdc.bin", "/binance_btc"), ("captures.txt", "/kraken_eth")):
            self.setUp()

            def planter(req, suivi, delai, tls, lire=self.faux({}), cible=cible, pendant=pendant):
                if req.chemin == pendant:
                    with open(os.path.join(self.d, cible), "wb") as f:
                        f.write(b"avant")
                return lire(req, suivi, delai, tls)
            with self.subTest(cible=cible):
                with self.assertRaises(FileExistsError):
                    capture.capturer([forme(d) for d in FORMES], [forme("kraken_eth")], (POOL, CARTE), self.d,
                                     lire=planter, pause=lambda s: None)
                self.assertEqual(self.lu(cible), b"avant")

    def test_commande_capture_rien_sur_la_sortie(self):
        """`capture --formes F [--carte C] --dossier D` : sortie 0 et rien d'imprimé ; refus (dossier absent) : 2,
        `capture : refus : …` sur l'erreur standard seule."""
        f, _s, _d = configurations(443)
        f["formes"] = [forme("binance_btc"), forme("okx_usdc_usdt")]
        ch = fichiers(self.d, formes=f, carte=carte(443, delai=250_000, formes=[forme("kraken_eth")]))
        os.mkdir(os.path.join(self.d, "c"))
        r = []
        with mock.patch.object(capture.http, "lire", side_effect=self.faux({})):
            for dossier in ("c", "absent"):
                out, err = io.StringIO(), io.StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    r.append((entree.main(["capture", "--formes", ch["formes"], "--carte", ch["carte"], "--dossier",
                                           os.path.join(self.d, dossier)]), out.getvalue(), err.getvalue()[:24]))
        self.assertEqual(r, [(0, "", ""), (2, "", "capture : refus : dossie")])
        self.assertEqual(sorted(os.listdir(os.path.join(self.d, "c"))), [
            "captures.txt", "carte-kraken-eth.bin", "pool-binance-btc.bin", "temoin-okx-usdc-usdt.bin"])


if __name__ == "__main__":
    unittest.main()
