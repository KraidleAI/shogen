"""RB-0 : paramètres d'analyse scellés. Octets VALIDE écrits à la main, sha256 par `sha256sum` hors du code (G1)."""
import json
import os
import tempfile
import unittest

from shogen_s2bis.recalc import config_analyse as ca

VALIDE = (b'{"degradation": {"d2_retard_s": 5, "d3_borne_s": 1, "d3_age_s": 120, "d4_echecs": 2, "d4_delai_s": 2, '
          b'"d5_echecs": 2, "d5_delai_s": 2}, "gardes": {"diviseur_n": 2, "k_crit": 2, "runs": 2, "unites": 2}, '
          b'"n_s": {"calme": 109440, "stress": 43776}, "p_j": {"grille": ["0.0025", "0.005", "0.01", "0.02"], '
          b'"seuil": "0.005"}, "rotations": {"R": 9999, "seuil": 99}, "t_max_s": 14515200, "tau_sigma": {"BTC": '
          b'{"agregateur": {"sigma": 300, "tau": "0.0265"}, "oracle_chainlink": {"sigma": 5400, "tau": "0.027"}, '
          b'"place_horodatee": {"sigma": 30, "tau": "0.005"}, "sans_horodatage": {"sigma": null, "tau": "0.013"}}, '
          b'"ETH": {"place_horodatee": {"sigma": 30, "tau": "0.0075"}}, "USDC": {"oracle_chainlink": {"sigma": 124200, '
          b'"tau": "0.00375"}}, "USDT": {"oracle_chainlink": {"sigma": 129600, "tau": "0.00375"}}}, '
          b'"tolerance_evenements": 20, "unites": {"BTC": ["api.binance.com", "api.kraken.com", '
          b'"ethereum-rpc.publicnode.com"], "ETH": ["api.kraken.com"], "USDC": ["api.kraken.com"], "USDT": '
          b'["api.binance.com"]}}\n')
SHA_VALIDE = "c75973684681536db5523b82e2d55d758fc5c62a1528611066b7430cebe7a15e"


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


class TauSigma(Base):                                        # bornes écrites d'après l'ADR-0029 l.181-183 et l.182
    def eth(self, classe, sigma, tau):
        return VALIDE.replace(b'"ETH": {"place_horodatee": {"sigma": 30, "tau": "0.0075"}}',
                              b'"ETH": {"' + classe + b'": {"sigma": ' + sigma + b', "tau": "' + tau + b'"}}')

    def test_bornes_de_tau(self):                            # 0,05 % <= τ < 2,85 % (E-R-09), fraction écrite
        for tau in (b"0.0005", b"0.02849999"):
            d = self.charger(self.eth(b"place_horodatee", b"30", tau))[0]
            self.assertEqual(d["tau_sigma"]["ETH"]["place_horodatee"]["tau"], tau.decode())
        self.refus([("ANALYSE/borne", self.eth(b"place_horodatee", b"30", t), "tau = " + t.decode())
                    for t in (b"0.0004999", b"0.0285", b"0.5")] +
                   [("ANALYSE/fraction", self.eth(b"place_horodatee", b"30", t), "tau = '" + t.decode())
                    for t in (b"5%", b"0.5e-3", b"-0.001", b".005", b"0.", b"0.000", b"1.0005")])

    def test_planchers_de_sigma(self):                       # 30, 300, 5 400 s ; aucun pour les places sans horodatage
        for classe, plancher in ((b"place_horodatee", 30), (b"agregateur", 300), (b"oracle_chainlink", 5400)):
            d = self.charger(self.eth(classe, str(plancher).encode(), b"0.01"))[0]
            self.assertEqual(d["tau_sigma"]["ETH"][classe.decode()]["sigma"], plancher)
            self.refus([("ANALYSE/sigma", self.eth(classe, s, b"0.01"), "sigma = " + d)
                        for s, d in ((str(plancher - 1).encode(), f"{plancher - 1} (plancher {plancher})"),
                                     (b"null", "None"), (b"true", "True"))])
        d = self.charger(self.eth(b"sans_horodatage", b"null", b"0.01"))[0]
        self.assertEqual(d["tau_sigma"]["ETH"], {"sans_horodatage": {"sigma": None, "tau": "0.01"}})
        self.refus((("ANALYSE/sigma", self.eth(b"sans_horodatage", b"0", b"0.01"), "sigma = 0 (plancher None)"),
                    ("ANALYSE/classe", VALIDE.replace(b'"ETH": {"place_horodatee": {"sigma": 30, "tau": "0.0075"}}',
                                                      b'"ETH": {}'), "$.tau_sigma.ETH : []")))


class Oracles(Base):                       # C-1 et Q-RB-4 de la G2 de RB-T1 ; ADR-0029 l.181, l.188 et l.189
    def ajout(self, entree):                                     # une classe de plus à ETH
        return VALIDE.replace(b'"ETH": {', b'"ETH": {' + entree + b", ")

    def test_planchers_de_sigma_par_actif(self):                 # C-1 : USDC 124 200 s, USDT 129 600 s (l.188)
        self.assertEqual([self.charger(VALIDE)[0]["tau_sigma"][a]["oracle_chainlink"]["sigma"] for a in (
            "BTC", "USDC", "USDT")], [5400, 124200, 129600])                    # planchers admis
        self.refus([("ANALYSE/sigma", VALIDE.replace(b'"sigma": ' + s, b'"sigma": ' + str(int(s) - 1).encode()),
                     f"{a}.oracle_chainlink.sigma = {int(s) - 1} (plancher {int(s)})")
                    for a, s in (("BTC", b"5400"), ("USDC", b"124200"), ("USDT", b"129600"))])

    def test_planchers_de_tau_des_oracles(self):                 # Q-RB-4 : 0,75 % pour ETH, 0,375 % stables (l.188)
        eth = self.ajout(b'"oracle_chainlink": {"sigma": 5400, "tau": "0.0075"}')
        btc = VALIDE.replace(b'"tau": "0.027"', b'"tau": "0.0005"')         # BTC : aucun plancher en valeur (l.181)
        self.assertEqual((self.charger(eth)[0]["tau_sigma"]["ETH"]["oracle_chainlink"]["tau"],
                          self.charger(btc)[0]["tau_sigma"]["BTC"]["oracle_chainlink"]["tau"]), ("0.0075", "0.0005"))
        r = VALIDE.replace
        self.refus([("ANALYSE/tau-plancher", o, d) for o, d in (
            (eth.replace(b'"0.0075"}, "place', b'"0.00749"}, "place'), "ETH.oracle_chainlink.tau = 0.00749 (plancher "
             "0.0075)"), (r(b'124200, "tau": "0.00375"', b'124200, "tau": "0.003749"'), "USDC.oracle_chainlink.tau = "
                          "0.003749 (plancher 0.00375)"),
            (r(b'129600, "tau": "0.00375"', b'129600, "tau": "0.0037"'), "USDT.oracle_chainlink.tau = 0.0037"))])

    def test_grille_de_tau_de_btc(self):                         # Q-RB-4 : grille de 0,05 % pour BTC seul (l.181)
        r = VALIDE.replace
        bords = r(b'"tau": "0.0265"', b'"tau": "0.028"').replace(b'"tau": "0.005"', b'"tau": "0.0005"')
        hors = r(b'"tau": "0.0075"', b'"tau": "0.00751"')        # ETH : grille du G0 de CALIB-ACTIFS (l.186)
        self.assertEqual((self.charger(bords)[0]["tau_sigma"]["BTC"]["agregateur"]["tau"],
                          self.charger(hors)[0]["tau_sigma"]["ETH"]["place_horodatee"]["tau"]), ("0.028", "0.00751"))
        self.refus([("ANALYSE/tau-grille", r(b'"tau": "' + a + b'"', b'"tau": "' + x + b'"'),
                     f"BTC.{c}.tau = {x.decode()}") for a, x, c in (
            (b"0.0265", b"0.02651", "agregateur"), (b"0.005", b"0.00525", "place_horodatee"),
            (b"0.013", b"0.0131", "sans_horodatage"), (b"0.027", b"0.0279", "oracle_chainlink"))])

    def test_sigma_au_moins_celui_de_btc(self):                  # Q-RB-4 : places et agrégateurs (l.189)
        agr = self.ajout(b'"agregateur": {"sigma": 300, "tau": "0.01"}')
        oracle = self.ajout(b'"oracle_chainlink": {"sigma": 5400, "tau": "0.0075"}').replace(
            b'5400, "tau": "0.027"', b'10800, "tau": "0.027"')   # l.188 : σ d'ETH = 1,5 × heartbeat, sous σ_BTC admis
        self.assertEqual((self.charger(agr)[0]["tau_sigma"]["ETH"]["agregateur"]["sigma"],
                          self.charger(oracle)[0]["tau_sigma"]["ETH"]["oracle_chainlink"]["sigma"]), (300, 5400))
        self.refus([("ANALYSE/incoherent", o, "incoherent : sigma-btc") for o in (
            agr.replace(b'"sigma": 300, "tau": "0.0265"', b'"sigma": 301, "tau": "0.0265"'),
            VALIDE.replace(b'"sigma": 30, "tau": "0.005"', b'"sigma": 31, "tau": "0.005"'),
            agr.replace(b'"agregateur": {"sigma": 300, "tau": "0.0265"}, ', b""))])      # classe absente de BTC


class Unites(Base):
    def test_noms_d_hote_en_minuscules(self):    # Q-RB-13 : a à z, 0 à 9, « - » et « . », de 1 à 253 caractères
        bords = VALIDE.replace(b'"BTC": [', b'"BTC": ["-", ".", "0", "' + b"a" * 253 + b'", ').replace(
            b'"ethereum-rpc.publicnode.com"]', b'"ethereum-rpc.publicnode.com", "z"]')
        self.assertEqual(self.charger(bords)[0]["unites"]["BTC"], ["-", ".", "0", "a" * 253, "api.binance.com",
                                                                  "api.kraken.com", "ethereum-rpc.publicnode.com", "z"])
        self.refus([("ANALYSE/unite", VALIDE.replace(b'"USDT": ["api.binance.com"]', b'"USDT": [' + n + b"]"), d)
                    for n, d in ((b'" !"', "' !'"), (b'"~"', "'~'"), (b'"Api.binance.com"', "'Api.binance.com'"),
                                 (b'"api binance.com"', "'api binance.com'"), (b'"a_b"', "'a_b'"),
                                 (b'"' + b"a" * 254 + b'"', "= '" + "a" * 254 + "'"), (b'"api:443"', "'api:443'"),
                                 (b'"\xc3\xa9"', "'\xe9'"), (b'"a\\tb"', "'a\\tb'"),
                                 (b'"a\\u007f"', "'a\\x7f'"), (b'"a\\u001f"', "'a\\x1f'"), (b"7", "= 7"))])


class Coherence(Base):
    def test_regles(self):
        r, alpha = VALIDE.replace, dict(ca.COHERENCE)["alpha"]           # alpha : seconde garde (Q-RB-6)
        self.assertEqual([alpha({"rotations": {"R": R, "seuil": s}}) for R, s in ((9999, 99), (999, 9), (99, 0), (
            9999, 98), (9999, 100), (9998, 99))], [True] * 3 + [False] * 3)     # (seuil + 1)/(R + 1) = 0,01 exactement
        self.assertEqual(self.charger(r(b'"seuil": "0.005"', b'"seuil": "0.0050"'))[0]["p_j"]["seuil"], "0.0050")
        self.refus([("ANALYSE/incoherent", o, "incoherent : " + nom) for nom, o in (
            ("t_max-grille", r(b"14515200", b"14515230")), ("p_j-seuil", r(b'"seuil": "0.005"', b'"seuil": "0.004"')),
            ("p_j-grille", r(b'"0.0025", "0.005"', b'"0.005", "0.0025"')),
            ("p_j-grille", r(b'"0.0025", "0.005"', b'"0.005", "0.005"')),
            ("unites-ordre", r(b'"api.binance.com", "api.kraken.com"', b'"api.kraken.com", "api.binance.com"')),
            ("unites-ordre", r(b'"api.binance.com", "api.kraken.com"', b'"api.binance.com", "api.binance.com"')),
            ("unites-btc", r(b'"ETH": ["api.kraken.com"]', b'"ETH": ["api.okx.com"]')))])

    def test_R_et_seuil_exacts(self):                         # Q-RB-6 : R = 9 999, seuil = 99 (l.139, l.200, l.202)
        self.refus([("ANALYSE/borne", VALIDE.replace(b'"R": 9999, "seuil": 99', x), d) for x, d in (
            (b'"R": 999, "seuil": 9', "R = 999"), (b'"R": 9998, "seuil": 99', "R = 9998"),
            (b'"R": 9999, "seuil": 98', "rotations.seuil = 98"), (b'"R": 9999, "seuil": 100', "seuil = 100"))])


class Gabarit(Base):                                         # s2bis/config/analyse.json, valeurs de l'ADR-0029
    def test_valeurs_de_l_adr_et_blocs_des_lots_amont(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config",
                               "analyse.json"), "rb") as f:
            octets = f.read()
        self.refus((("ANALYSE/a-fixer", octets, "a-fixer : n_s, t_max_s, tau_sigma, tolerance_evenements, unites"),))
        g = json.loads(octets)
        self.assertEqual({k: g[k] for k in ("degradation", "gardes", "p_j", "rotations")}, {
            "degradation": {"d2_retard_s": 5, "d3_borne_s": 1, "d3_age_s": 120, "d4_echecs": 2, "d4_delai_s": 2,
                            "d5_echecs": 2, "d5_delai_s": 2},                     # l.107-110 ; l.397 (3)
            "gardes": {"unites": 2, "k_crit": 2, "runs": 2, "diviseur_n": 2},      # l.203 : n′_s >= n_s/2
            "p_j": {"seuil": "0.005", "grille": ["0.0025", "0.005", "0.01", "0.02"]},          # l.212
            "rotations": {"R": 9999, "seuil": 99}})                                # l.139, l.200, l.202
        v = json.loads(VALIDE)                                  # complété par les blocs synthétiques : accepté
        g.update({k: v[k] for k in ("n_s", "t_max_s", "tau_sigma", "tolerance_evenements", "unites")})
        self.assertEqual(self.charger(json.dumps(g).encode())[0], g)
