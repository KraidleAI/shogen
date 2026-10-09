"""Calcul d'un actif et fragment pour analyse.json (T-CA-FRG-1 ; E-CA-17, E-CA-22, E-CA-23 côté lot) sur séries
synthétiques ; chargeur de la configuration d'analyse (s2bis/shogen_s2bis/recalc/config_analyse.py, lu, jamais modifié)
sur s2bis/config/analyse.json complété d'un bloc BTC synthétique. Chaque test nomme la mutation qui le rougit."""
import json
import os
import shutil
import tempfile
import unittest
from decimal import Decimal

import socle
import tau
from tests import synthetiques as sy
from tests.test_fenetre import config_analyse

P = socle.lire()
BTC_BLOC = {"agregateur": {"sigma": 900, "tau": "0.0265"}, "oracle_chainlink": {"sigma": 10800, "tau": "0.0270"},
            "place_horodatee": {"sigma": 90, "tau": "0.0045"}, "sans_horodatage": {"sigma": None, "tau": "0.0050"}}


def resultats(prm=P):
    return {a: tau.calcul_actif(prm, a, sy.series(prm, a), sy.FEN, sy.BTC) for a in socle.ACTIFS}


class TestFragment(unittest.TestCase):
    def test_fragment_charge(self):
        """T-CA-FRG-1 : fragment complété par un bloc BTC synthétique et les champs encore à null (n_s, t_max_s,
        tolérance) : config_analyse.charger l'accepte ; modes « calibre » ; σ des places sans horodatage null ; τ égal
        pour les deux classes de places ; unités de parametres.json. Mutation : σ entier rendu en chaîne."""
        frag = tau.fragment(P, resultats())
        with open(os.path.join(socle.RACINE, "s2bis", "config", "analyse.json"), encoding="utf-8") as f:
            a = json.load(f)
        a.update(n_s={"calme": 1000, "stress": 500}, t_max_s=600, tolerance_evenements=0,
                 tau_sigma={"BTC": BTC_BLOC} | frag["tau_sigma"], unites={"BTC": P["unites"]["ETH"]} | frag["unites"])
        d = tempfile.mkdtemp(prefix="ca_frg_")
        self.addCleanup(shutil.rmtree, d, True)
        with open(os.path.join(d, "analyse.json"), "w", encoding="utf-8") as f:
            json.dump(a, f)
        donnees, _sha = config_analyse.charger(f.name)
        self.assertEqual((frag["modes"], donnees["unites"]["USDC"]), (dict.fromkeys(socle.ACTIFS, "calibre"),
                                                                     P["unites"]["USDC"]))
        for x in frag["tau_sigma"].values():
            self.assertEqual((x["sans_horodatage"]["sigma"], x["sans_horodatage"]["tau"]),
                             (None, x["place_horodatee"]["tau"]))

    def test_controle_fragment(self):
        """Fragment rejoué (E-CA-23 côté lot) : τ_agr hors grille (a) ou décalé d'un pas (d), τ des places hors grille
        (b), τ d'oracle arrondi (c), σ des agrégateurs ou des oracles décalé (e, f), σ des places sans horodatage posé
        (g), τ des places différent entre classes (h) : CA/fragment, la règle nommée. Mutation M-CA-22 : fragment non
        contrôlé (chaque règle retirée à son tour)."""
        frag = tau.fragment(P, resultats())
        tau.controle_fragment(P, frag, sy.BTC)
        cas = {"a": ("agregateur", "tau", lambda v: str(Decimal(v) + Decimal("0.0001"))),
               "d": ("agregateur", "tau", lambda v: str(Decimal(v) + Decimal("0.0005"))),
               "b": ("place_horodatee", "tau", lambda v: str(Decimal(v) + Decimal("0.0001"))),
               "c": ("oracle_chainlink", "tau", lambda v: "0.0080"), "e": ("agregateur", "sigma", lambda v: v + 1),
               "f": ("oracle_chainlink", "sigma", lambda v: v - 60), "g": ("sans_horodatage", "sigma", lambda v: 30),
               "h": ("sans_horodatage", "tau", lambda v: str(Decimal(v) + Decimal("0.0005")))}
        for regle, (classe, cle, f) in cas.items():
            g = json.loads(json.dumps(frag))
            g["tau_sigma"]["USDT"][classe][cle] = f(g["tau_sigma"]["USDT"][classe][cle])
            with self.assertRaises(socle.Refus) as r:
                tau.controle_fragment(P, g, sy.BTC)
            self.assertIn(f"({regle})", str(r.exception), regle)

    def test_planchers_seuls(self):
        """Mode « planchers seuls » pour USDT (F3) : τ des places 0,00375, hors grille admis, τ_agr = grid-ceil(0,00375
        × 0,0265 / 0,0050) = 0,0200 (0,019875 arrondi au-dessus), σ des places horodatées sans le troisième terme (180
        s, calculé et écarté) : 90 s ; le contrôle (b) l'admet ; même τ_agr sous BTC_PH (τ_ph > τ_sh, C-1 : 0,0225 sous
        la seule classe sans horodatage, 0,022083… arrondi). Mutations : mode ignoré ; G01 ; G02."""
        q = json.loads(json.dumps(P))
        q["lectures"]["A"]["modes"]["USDT"] = "planchers_seuls"
        for btc in (sy.BTC_PH, sy.BTC):
            r = tau.calcul_actif(q, "USDT", sy.series(q, "USDT"), sy.FEN, btc)
            self.assertEqual((r["places"]["tau"], r["agregateurs"]["tau"], r["sigma"]["place_horodatee"]),
                             (Decimal("0.00375"), Decimal("0.0200"), 90))
        self.assertEqual(r["terme"], 180)                     # coinbase sans échange une minute : 3 × 1 × 60 s, écarté
        tau.controle_fragment(q, tau.fragment(q, {"USDT": r}), sy.BTC)


    def test_site_exclusion(self):
        """Site d'appel (SHOGEN-MUTANTS-SITE-APPEL-1) : calcul_actif passe à ecarts l'exclusion {coinbase : σ des places
        horodatées de l'actif} pour ETH, et {} pour USDC (aucune place à dernière transaction). Mutation : exclusion
        non transmise."""
        vus, ecarts = [], tau.ecarts
        tau.ecarts = lambda *a: vus.append(a[5]) or ecarts(*a)
        self.addCleanup(setattr, tau, "ecarts", ecarts)
        r = [tau.calcul_actif(P, a, sy.series(P, a), sy.FEN, sy.BTC) for a in ("ETH", "USDC")]
        self.assertEqual(vus, [{"coinbase": r[0]["sigma"]["place_horodatee"]}, {}])

    def test_borne_basse_et_variante(self):
        """C-8 : six places au même prix, écarts nuls : règle 0, τ des places 0,0005 (borne basse, drapeau) ; τ_agr
        calculé sur 0,0005 : 0,0005 × 0,0265 / 0,0050 = 0,00265, soit 0,0030. C-11 : lecture A-prime, USDC sur trois
        places (binance, bitstamp, kraken) à N_min 3 : 5 minutes × 3 places par strate. Mutations : G23 (τ_agr sur la
        valeur de la règle) ; G27 (N_min codé à 4)."""
        egal = {p: {t: (Decimal(100), True) for t in socle.minutes(sy.FEN)} for p in socle.lecture(P)["places"]["ETH"]}
        r = tau.calcul_actif(P, "ETH", egal, sy.FEN, sy.BTC)
        self.assertEqual((r["places"]["regle"], r["places"]["tau"], r["places"]["drapeau"], r["agregateurs"]["tau"]),
                         (0, Decimal("0.0005"), "borne basse appliquée", Decimal("0.0030")))
        q = json.loads(json.dumps(P))
        q["lecture"] = "A-prime"
        try:
            cel = tau.calcul_actif(q, "USDC", sy.series(q, "USDC"), sy.FEN, sy.BTC)["cellules"]
        except socle.Refus as e:                                    # rouge d'assertion sous la mutation G27
            cel = {str(e): ((), (), ())}
        self.assertEqual({st: len(e) for st, (e, _p, _a) in cel.items()}, {"calme": 15, "stress": 15})


if __name__ == "__main__":
    unittest.main()
