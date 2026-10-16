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

    def test_borne_valeur(self):
        """C-13 (O-1) : refus CA/borne au calcul (borne haute abaissée à 0,0015) : valeur calculée de la règle sur une
        ligne à part de calib_actifs.txt, nommée et descriptive, après le refus, égale à la règle du calcul direct sous
        la borne scellée ; refus et fragment JSON sans valeur (§5.7). SHOGEN-CALIB-BORNE-MULTI-1 : les trois actifs
        touchent cette borne, une ligne chacun dans l'ordre des actifs. Mutations : ligne omise ; valeur d'une autre
        règle ; calcul arrêté au premier refus."""
        argv, d = banc(self, lambda p: p["tau"].update(borne_haute_exclue="0.0015"))
        self.assertEqual(tau.main(argv, {}), 1)
        texte, frag = lire(d)
        p = socle.lire()
        refus = "REFUS CA/borne : τ des places à la borne haute exclue ou au-delà ; actif ETH"
        valeurs = [("descriptif hors refus (jamais décisif) : valeur calculée de la règle, τ des places : "
                    f"{tau.calcul_actif(p, a, sy.series(p, a), sy.FEN, sy.BTC)['places']['regle']} ; actif {a}")
                   for a in socle.ACTIFS]
        self.assertEqual((texte[1:], frag["refus"]), ([refus, *valeurs, ""], refus))

    def test_borne_plusieurs(self):
        """SHOGEN-CALIB-BORNE-MULTI-1 (O-CC-2), sous la borne scellée (0,0285). ETH et USDT au prix 100 sur cinq places
        et 102 ou 103 sur okx (ou 100), toutes minutes actives : seule okx s'écarte de la médiane leave-one-out (100),
        de 0,02 ou 0,03 ; P99,9 = maximum ; règle 1,5 × 0,02 = 0,0300 et 1,5 × 0,03 = 0,0450 (valeurs à la main),
        au-delà de 0,0285 ; six places à 100 : sous la borne basse, aucun refus. USDC (séries synthétiques) passe.
        Par passe : le refus du premier actif refusé dans les deux sorties, une ligne de valeur par actif à la borne
        dans l'ordre des actifs, puis une ligne par refus suivant sans valeur (C-B4 de la G2 de DETTES-T1 : exception
        non nommée en CA/calcul, type seul), aucun fragment. Passes : deux à la borne ; USDC en exception non nommée ;
        ordre des actifs contraire à l'ordre des valeurs (C-B3) ; un seul actif refusé (C-B1) ; premier refus sans
        valeur (CA/population injecté) puis CA/borne (C-B2) ; CA/borne puis CA/population (C-B4) ; deux refus suivants,
        dans l'ordre des actifs (C-B6) ; exception non nommée au premier actif : refus écrit sans actif (C-B7) ; refus
        global aux paramètres (plancher d'oracle d'USDT faux : CA/chainlink à chaque actif, levé au calcul de σ) ou
        injecté identique sur USDC et USDT : une ligne de refus suivant par texte, aucune qui répète le refus écrit
        (C-B8). Mutations : arrêt au premier refus ; refus unique non levé (MB03) ; lignes seulement si le refus écrit
        porte une valeur (MB01) ; lignes triées par valeur (MB10) ; refus suivants non imprimés, imprimés avec le
        premier refus, réduits au premier (NB2) ou inversés (NB3) ; actif au refus écrit CA/calcul (NB4) ; refus
        suivants répétés. C-B9 (R-4) : passe « même motif » (CA/population en strate calme pour ETH et USDC, celui
        d'ETH répété par USDT) : le refus d'USDC gardé, celui d'ETH jamais répété ; mutations ND1 (dédoublonnage par
        code et motif, actif ignoré) et ND2 (dédoublonnage contre le dernier texte seul)."""
        orig = tau.calcul_actif

        def injecte(vise, exc, suite=None):
            def f(prm, actif, *x):
                if actif == vise:
                    raise exc
                return (suite or orig)(prm, actif, *x)
            return f
        p = socle.lire()
        borne = "REFUS CA/borne : τ des places à la borne haute exclue ou au-delà ; actif "
        pop = "REFUS CA/population : aucune cellule à N_min places définies ; actif "
        hors = "descriptif hors refus (jamais décisif) : valeur calculée de la règle, τ des places : "
        suivant = "descriptif hors refus (jamais décisif) : refus suivant : "
        calcul = "REFUS CA/calcul : calcul en échec (ZeroDivisionError)"
        chainlink = ("REFUS CA/chainlink : plancher d'oracle différent de la valeur attendue ; actif USDT ; classe "
                     "oracle_chainlink")

        def pop_de(actif):
            return socle.Refus("CA/population", "aucune cellule à N_min places définies", actif, strate="calme")

        def faux(q):
            q["oracles_attendus"]["tau"]["USDT"] = "0.9"
        globale = socle.Refus("CA/chainlink", "plancher d'oracle différent de la valeur attendue", "USDT",
                              "oracle_chainlink")
        cas = [("deux", orig, 102, 103, borne + "ETH", [hors + "0.0300 ; actif ETH", hors + "0.0450 ; actif USDT"]),
               ("exception", injecte("USDC", ZeroDivisionError()), 102, 103, borne + "ETH",
                [hors + "0.0300 ; actif ETH", hors + "0.0450 ; actif USDT",
                 suivant + "REFUS CA/calcul : calcul en échec (ZeroDivisionError) ; actif USDC"]),
               ("ordre", orig, 103, 102, borne + "ETH", [hors + "0.0450 ; actif ETH", hors + "0.0300 ; actif USDT"]),
               ("seul", orig, 100, 103, borne + "USDT", [hors + "0.0450 ; actif USDT"]),
               ("sans valeur", injecte("ETH", socle.Refus("CA/population", "aucune cellule à N_min places définies",
                                                          "ETH", strate="calme")), 102, 103,
                pop + "ETH ; strate calme", [hors + "0.0450 ; actif USDT"]),
               ("suivant", injecte("USDT", socle.Refus("CA/population", "aucune cellule à N_min places définies",
                                                       "USDT", strate="stress")), 102, 103, borne + "ETH",
                [hors + "0.0300 ; actif ETH", suivant + pop + "USDT ; strate stress"]),
               ("deux suivants", injecte("USDC", ZeroDivisionError(), injecte("USDT", socle.Refus(
                   "CA/population", "aucune cellule à N_min places définies", "USDT", strate="stress"))), 102, 103,
                borne + "ETH", [hors + "0.0300 ; actif ETH", suivant + calcul + " ; actif USDC",
                                suivant + pop + "USDT ; strate stress"]),
               ("exception premier", injecte("ETH", ZeroDivisionError()), 102, 103, calcul,
                [hors + "0.0450 ; actif USDT"]),
               ("doublon", injecte("USDC", globale, injecte("USDT", globale)), 102, 103, borne + "ETH",
                [hors + "0.0300 ; actif ETH", suivant + chainlink]),
               ("global", orig, 100, 100, chainlink, [], faux),
               ("même motif", injecte("ETH", pop_de("ETH"), injecte("USDC", pop_de("USDC"), injecte(
                   "USDT", pop_de("ETH")))), 102, 103, pop + "ETH ; strate calme",
                [suivant + pop + "USDC ; strate calme"])]
        for nom, calcul_, eth, usdt, refus, lignes, *modif in cas:
            with self.subTest(nom):
                argv, d = banc(self, *modif)
                for actif, okx in (("ETH", eth), ("USDT", usdt)):
                    for x in socle.lecture(p)["places"][actif]:
                        s = {t: (socle.Decimal(okx if x == "okx" else 100), True) for t in socle.minutes(sy.FEN)}
                        for n, o in sy.fichiers(p, x, s).items():
                            with open(os.path.join(argv[1], "principale", x, actif, n), "wb") as f:
                                f.write(o)
                tau.calcul_actif = calcul_
                try:
                    code = tau.main(argv, {})
                finally:
                    tau.calcul_actif = orig
                self.assertEqual((code, *lire(d)), (1, [socle.ETIQUETTE, refus, *lignes, ""],
                                                    {"etiquette": socle.ETIQUETTE, "refus": refus}))


if __name__ == "__main__":
    unittest.main()
