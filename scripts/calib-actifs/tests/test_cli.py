"""Point d'entrée du calcul (tau.py ; E-CA-04, E-CA-17, E-CA-19, E-CA-22) sur bruts synthétiques aux six formats et un
tau_sigma.txt synthétique (jamais le vrai) ; comptes de l'oracle réduits à la fenêtre synthétique, calculés à la main :
binance actif 9 minutes sur 10 ; USDC à au moins 4, 3, 2 places actives : 3, 10, 10. Chaque test nomme sa mutation."""
import contextlib
import io
import json
import os
import shutil
import tempfile
import unittest

import socle
import tau
from tests import synthetiques as sy

DESC = {"debut": 1788566100, "fin": 1788566700, "sans": ["kraken"], "source": ""}     # 2026-09-04 23:55 à 09-05 00:05


def banc(test, modif=None):
    """(argv, dossier de sortie) : bruts synthétiques des deux fenêtres, tau_sigma synthétique épinglé, parametres
    du lot ramenés à la fenêtre synthétique (modif(prm) éventuel)."""
    d = tempfile.mkdtemp(prefix="ca_cli_")
    test.addCleanup(shutil.rmtree, d, True)
    prm = socle.json.loads(socle.json.dumps(socle.lire()))
    ts = os.path.join(d, "tau_sigma.txt")
    with open(ts, "w", encoding="utf-8") as f:
        f.write(socle.NL.join(["étiquette", socle.BLOC, *(f"{k} {c} {v}" for (k, c), v in sy.BTC.items()),
                               "tau oracle_chainlink 0.0270", "sigma sans_horodatage aucun"]) + socle.NL)
    prm.update(fenetre=dict(sy.FEN, source=""), fenetre_descriptive=DESC,
               plan_s2bis={"tau_sigma": ts, "sha256": socle.empreinte(ts), "source": ""},
               oracle_sh={"debut": sy.FEN["debut"], "fin": sy.FEN["fin"], "actives": [["USDC", "binance", 9]],
                          "concurrences": [["USDC", ["binance", "bitfinex", "bitstamp", "kraken"], [3, 10, 10]]],
                          "source": ""})
    if modif:
        modif(prm)
    for nom, fen in (("principale", sy.FEN), ("descriptive", DESC)):
        sy.ecrire_bruts(prm, os.path.join(d, "b"), nom, fen)
    with open(os.path.join(d, "p.json"), "w", encoding="utf-8") as f:
        json.dump(prm, f)
    return ["--bruts", os.path.join(d, "b"), "--sortie", os.path.join(d, "s"), "--parametres", f.name], d


def decale(frag):
    """τ des agrégateurs d'ETH décalé d'un pas (0,0005)."""
    x = frag["tau_sigma"]["ETH"]["agregateur"]
    x["tau"] = str(socle.Decimal(x["tau"]) + socle.Decimal("0.0005"))
    return frag


def lire(d):
    with open(os.path.join(d, "s", "calib_actifs.txt"), encoding="utf-8") as f:
        texte = f.read().split(socle.NL)
    with open(os.path.join(d, "s", "fragment_analyse.json"), encoding="utf-8") as g:
        return texte, json.load(g)


class TestCli(unittest.TestCase):
    def test_succes(self):
        """Code 0 ; texte à l'étiquette mot pour mot, blocs [VALEURS] et [DESCRIPTIFS], septembre par actif (USDC refusé
        : trois places sans kraken, sous N_min) ; bloc [VALEURS] égal au calcul direct sur les séries de chaque actif ;
        fragment JSON à la clé « etiquette », égal au fragment calculé directement ; aucun .partiel. Mutations : oracle
        non appelé ; septembre omis ; étiquette absente du JSON ; séries ou valeurs de BTC d'une autre source."""
        argv, d = banc(self)
        self.assertEqual(tau.main(argv, {}), 0)
        texte, frag = lire(d)
        self.assertEqual((texte[0], frag.pop("etiquette")), (socle.ETIQUETTE, socle.ETIQUETTE))
        self.assertTrue({"[VALEURS]", "[DESCRIPTIFS]"} <= set(texte))
        self.assertTrue(any(x.startswith("oracle de SH") for x in texte))
        self.assertEqual([x.split(" : ")[1][:12] for x in texte if " septembre : " in x],
                         ["τ des places", "REFUS CA/pop", "τ des places"])
        self.assertEqual(sorted(os.listdir(os.path.join(d, "s"))), list(tau.SORTIES))
        with open(argv[5], encoding="utf-8") as f:
            prm = json.load(f)
        direct = {a: tau.calcul_actif(prm, a, sy.series(prm, a), sy.FEN, sy.BTC) for a in socle.ACTIFS}
        self.assertEqual(texte[texte.index("[VALEURS]") + 1:texte.index("[DESCRIPTIFS]")], tau.corps(prm, direct))

    def test_refus(self):
        """Code 1 et le même refus dans les deux sorties : compte de l'oracle faux (CA/oracle-sh), variable posée,
        épingle de tau_sigma fausse, exception non nommée (CA/calcul, type seul), fragment altéré (CA/fragment, site
        d'appel du contrôle) ; arguments faux : code 2. Mutations : refus sans sortie ; exception nommée par son message
        ; usage non contrôlé ; contrôle du fragment non appelé."""
        cas = [(lambda p: p["oracle_sh"]["actives"][0].__setitem__(2, 8), {}, "CA/oracle-sh"),
               (None, {"SHOGEN_S2_CAMPAGNE_CONTROL": "x"}, "CA/variable"),
               (lambda p: p["plan_s2bis"].update(sha256="0" * 64), {}, "CA/plan-s2bis")]
        for modif, env, code in cas:
            argv, d = banc(self, modif)
            self.assertEqual(tau.main(argv, env), 1)
            texte, frag = lire(d)
            self.assertEqual((texte[1].split(" : ")[0], frag["refus"].split(" : ")[0]), ("REFUS " + code,) * 2)
        for cible, f, code in ((tau, "fragment", "CA/fragment"), (tau.bougies, "oracle_sh", "CA/calcul")):
            argv, d = banc(self)
            orig = getattr(cible, f)
            setattr(cible, f, (lambda *x: decale(orig(*x))) if f == "fragment" else (lambda *x: 1 / 0))
            try:
                self.assertEqual(tau.main(argv, {}), 1)
            finally:
                setattr(cible, f, orig)
            refus = lire(d)[1]["refus"]
            self.assertEqual((refus.split(" : ")[0], refus.endswith("(ZeroDivisionError)")),
                             ("REFUS " + code, code == "CA/calcul"))
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual([tau.main(x, {}) for x in (["--bruts", d], argv[:4] + ["--x", argv[5]])], [2, 2])
        self.assertEqual(err.getvalue().count("REFUS CA/usage"), 2)


if __name__ == "__main__":
    unittest.main()
