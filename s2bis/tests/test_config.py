"""CB-0, E-C-02 : configurations scellées. Références écrites à la main (octets, codes et détails des refus nommés) ;
sha256 des octets VALIDE calculé hors du code, par `sha256sum` (journal G1 de CB-0)."""
import os
import tempfile
import unittest

from shogen_s2bis.collecte import config as c

SCHEMA = {"w": (int, 1, 3600), "nom": (str, 1, 8), "arme": (bool, None, None),
          "formes": [{"hote": (str, 1, 64), "n": (int, 1, 5)}]}
FORMES = b'[{"hote": "a.example", "n": 5}]'
VALIDE = b'{"w": 60, "nom": "pool", "arme": false, "formes": ' + FORMES + b'}\n'
SHA_VALIDE = "2485d525eaabd6955347800c93a3884ff229fceb6488910d6c8720753fbf2fa2"
PAIR = (("w-pair", lambda d: d["w"] % 2 == 0),)


class Config(unittest.TestCase):
    def charger(self, octets, coherence=()):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        with open(os.path.join(d.name, "c.json"), "wb") as f:
            f.write(octets)
        return c.charger(f.name, SCHEMA, coherence)

    def test_valide_sha256_des_octets_lus(self):
        donnees, sha = self.charger(VALIDE)
        self.assertEqual((donnees["w"], donnees["arme"], donnees["formes"][0]["hote"], sha),
                         (60, False, "a.example", SHA_VALIDE))

    def test_bornes_incluses(self):
        for v in (1, 3600):
            self.assertEqual(self.charger(VALIDE.replace(b"60", str(v).encode()))[0]["w"], v)

    def test_refus_nommes(self):
        r = VALIDE.replace
        for code, octets, detail in (
                ("CONFIG/champ-absent", r(b'"w": 60, ', b""), "$ : w"),
                ("CONFIG/champ-inconnu", r(b"{", b'{"x": 1, ', 1), "$ : x"),
                ("CONFIG/type", r(b"false", b"0"), "$.arme"), ("CONFIG/type", r(b"60", b"true"), "$.w : int"),
                ("CONFIG/type", b"[1]", "$ : objet"), ("CONFIG/type", r(FORMES, b"[]"), "$.formes"),
                ("CONFIG/borne", r(b"60", b"3601"), "$.w = 3601"), ("CONFIG/borne", r(b"60", b"0"), "$.w = 0"),
                ("CONFIG/borne", r(b'"pool"', b'"pool-long"'), "$.nom"), ("CONFIG/borne", r(b": 5}", b": 6}"), "[0].n"),
                ("CONFIG/borne", r(b"60", b"1" * 5000), "5000"), ("CONFIG/cle-double", r(b"{", b'{"w": 60, ', 1), "w"),
                ("CONFIG/borne", r(b"60", b"1" * 31), "entier de 31 chiffres"),     # C-5 (G-20) : 31 refusé à la
                ("CONFIG/borne", r(b"60", b"1" * 30), "$.w = 1111"),                # lecture, 30 lu puis hors schéma
                ("CONFIG/non-fini", r(b"60", b"NaN"), "NaN"), ("CONFIG/flottant", r(b"60", b"60.0"), "60.0"),
                ("CONFIG/json", b"\xff", "utf-8"), ("CONFIG/json", b"{", ""),
                ("CONFIG/json", b"[" * 100000 + b"]" * 100000, "recursion")):
            with self.subTest(code=code, octets=octets[:40]):
                with self.assertRaises(c.RefusConfig) as e:
                    self.charger(octets)
                self.assertEqual(e.exception.code, code)
                self.assertIn(detail, str(e.exception))

    def test_coherence(self):
        self.assertEqual(self.charger(VALIDE, PAIR)[1], SHA_VALIDE)
        with self.assertRaises(c.RefusConfig) as e:
            self.charger(VALIDE.replace(b"60", b"61"), PAIR)
        self.assertEqual((e.exception.code, str(e.exception)), ("CONFIG/incoherent", "CONFIG/incoherent : w-pair"))
