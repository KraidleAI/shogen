"""RB-0 : paramètres d'analyse scellés. Octets VALIDE écrits à la main, sha256 par `sha256sum` hors du code (G1)."""
import os
import tempfile
import unittest

from shogen_s2bis.recalc import config_analyse as ca

VALIDE = (b'{"degradation": {"d2_retard_s": 5, "d3_borne_s": 1, "d3_age_s": 120, "d4_echecs": 2, "d4_delai_s": 2, '
          b'"d5_echecs": 2, "d5_delai_s": 2}, "gardes": {"diviseur_n": 2, "k_crit": 2, "runs": 2, "unites": 2}, '
          b'"n_s": {"calme": 109440, "stress": 43776}, "p_j": {"grille": ["0.0025", "0.005", "0.01", "0.02"], '
          b'"seuil": "0.005"}, "rotations": {"R": 9999, "seuil": 99}, "t_max_s": 14515200, "tau_sigma": {"BTC": '
          b'{"agregateur": {"sigma": 300, "tau": "0.0265"}, "oracle_chainlink": {"sigma": 5400, "tau": "0.027"}, '
          b'"place_horodatee": {"sigma": 180, "tau": "0.005"}, "sans_horodatage": {"sigma": null, "tau": "0.013"}}, '
          b'"ETH": {"place_horodatee": {"sigma": 30, "tau": "0.0075"}}, "USDC": {"oracle_chainlink": {"sigma": 124200, '
          b'"tau": "0.00375"}}, "USDT": {"oracle_chainlink": {"sigma": 129600, "tau": "0.00375"}}}, '
          b'"tolerance_evenements": 20, "unites": {"BTC": ["api.binance.com", "api.kraken.com", '
          b'"ethereum-rpc.publicnode.com"], "ETH": ["api.kraken.com"], "USDC": ["api.kraken.com"], "USDT": '
          b'["api.binance.com"]}}\n')
SHA_VALIDE = "fcf18be56b5e16c965b39b9829210079d2ae602ba885cda1fdb60831d879cd14"


class Base(unittest.TestCase):
    def charger(self, octets):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        with open(os.path.join(d.name, "analyse.json"), "wb") as f:
            f.write(octets)
        return ca.charger(f.name)

    def refus(self, cas):
        for code, octets, detail in cas:
            with self.subTest(code=code, detail=detail):
                with self.assertRaises(ca.RefusAnalyse) as e:
                    self.charger(octets)
                self.assertEqual((e.exception.code, detail in str(e.exception)), (code, True), str(e.exception))


class Lecture(Base):
    def test_valide_et_sha256_des_octets_lus(self):
        d, sha = self.charger(VALIDE)
        self.assertEqual((d["rotations"]["R"], d["tau_sigma"]["BTC"]["sans_horodatage"], d["unites"]["ETH"], sha),
                         (9999, {"sigma": None, "tau": "0.013"}, ["api.kraken.com"], SHA_VALIDE))

    def test_refus_nommes(self):                             # JSON strict, blocs à fixer d'abord, puis schéma
        r, b = VALIDE.replace, "ANALYSE/borne"
        self.refus((("ANALYSE/cle-double", r(b'"d2_retard_s": 5', b'"d2_retard_s": 5, "d2_retard_s": 6'), "d2_"),
                    ("ANALYSE/flottant", r(b"120", b"120.0"), "120.0"), ("ANALYSE/non-fini", r(b"120", b"NaN"), "NaN"),
                    (b, r(b"14515200", b"9" * 31), "entier de 31 chiffres"), ("ANALYSE/json", VALIDE[:-3], ""),
                    ("ANALYSE/json", r(b"{", b"\xff{", 1), "utf-8"), ("ANALYSE/type", b"[1]\n", "objet"),
                    ("ANALYSE/json", b"[" * 100000 + b"]" * 100000, "recursion"),
                    ("ANALYSE/a-fixer", r(b"14515200", b"null").replace(b"evenements\": 20", b"evenements\": null"),
                     "a-fixer : t_max_s, tolerance_evenements"),
                    ("ANALYSE/champ-inconnu", r(b"{", b'{"x": null, ', 1), "$ : x"), (b, r(b"120", b"0"), "age_s = 0"),
                    ("ANALYSE/type", r(b'"calme": 109440', b'"calme": null'), "$.n_s.calme : int"),
                    ("ANALYSE/champ-absent", r(b'"runs": 2, ', b""), "gardes : runs"),
                    ("ANALYSE/type", r(b'"k_crit": 2', b'"k_crit": true'), "k_crit : int"),
                    ("ANALYSE/type", r(b'["api.kraken.com"], "USDC"', b'[], "USDC"'), "$.unites.ETH : liste"),
                    ("ANALYSE/unite", r(b'["api.kraken.com"], "USDC"', b'[""], "USDC"'), "ETH[0] = ''"),
                    ("ANALYSE/classe", r(b'"ETH": {"place_horodatee"', b'"ETH": {"oracle_pyth"'), "['oracle_pyth']"),
                    ("ANALYSE/fraction", r(b'"0.0075"', b'0'), "ETH.place_horodatee.tau = 0"),
                    ("ANALYSE/champ-inconnu", r(b'{"sigma": 30, ', b'{"sigma": 30, "x": 1, '), "place_horodatee : x"),
                    (b, r(b'"d4_echecs": 2', b'"d4_echecs": 4'), "d4_echecs = 4"),
                    (b, r(b'"d5_echecs": 2', b'"d5_echecs": 3'), "d5_echecs = 3"),
                    (b, r(b'"R": 9999', b'"R": 10000'), "R = 10000"), (b, r(b'"R": 9999', b'"R": 0'), "R = 0"),
                    (b, r(b'"seuil": 99', b'"seuil": -1'), "rotations.seuil = -1"),
                    (b, r(b'"stress": 43776', b'"stress": 0'), "stress = 0"), (b, r(b"14515200", b"0"), "t_max_s = 0"),
                    (b, r(b'evenements": 20', b'evenements": -1'), "tolerance_evenements = -1")))

    def test_bornes_admises(self):
        o = VALIDE
        for avant, apres in ((b'"d4_echecs": 2', b'"d4_echecs": 3'), (b'"d5_echecs": 2', b'"d5_echecs": 1'),
                             (b'"calme": 109440', b'"calme": 1'), (b'evenements": 20', b'evenements": 0'),
                             (b"14515200", b"60")):
            o = o.replace(avant, apres)
        d = self.charger(o)[0]
        self.assertEqual((d["degradation"]["d4_echecs"], d["degradation"]["d5_echecs"], d["n_s"]["calme"],
                          d["tolerance_evenements"], d["t_max_s"]), (3, 1, 1, 0, 60))
