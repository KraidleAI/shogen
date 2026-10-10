"""Socle : variable de campagne, lecture stricte de parametres.json, lecture retenue, épingle et bloc machine de
tau_sigma.txt (E-CA-02, E-CA-03, E-CA-06, E-CA-12, E-CA-24) ; le vrai tau_sigma.txt n'est que haché ou copié.
Attendus écrits à la main (date -u -d, sha256sum) ; chaque test nomme la mutation qui le rougit."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest

import socle


def ecrire_prm(test, modif, texte=None):
    """parametres.json du lot modifié par modif(dict), ou texte brut, dans un dossier jetable ; rend son chemin."""
    with open(socle.PARAMETRES, encoding="utf-8") as f:
        p = json.load(f)
    modif(p)
    d = tempfile.mkdtemp(prefix="ca_prm_")
    test.addCleanup(shutil.rmtree, d, True)
    with open(os.path.join(d, "p.json"), "w", encoding="utf-8") as f:
        f.write(texte or json.dumps(p))
    return f.name


class TestSocle(unittest.TestCase):
    def assertRefus(self, code, f, *a):
        with self.assertRaises(socle.Refus) as r:
            f(*a)
        self.assertEqual(r.exception.code, code)
        return str(r.exception)

    def test_variable(self):
        """T-CA-SOC-2 : environnement passé en argument ; la variable posée, même vide : CA/variable ; absente :
        aucun refus. Mutation M-CA-02 : garde retirée."""
        self.assertRefus("CA/variable", socle.garde, {"SHOGEN_S2_CAMPAGNE_CONTROL": ""})
        self.assertIsNone(socle.garde({"PATH": "/usr/bin"}))

    def test_parametres_lus(self):
        """Fenêtre 1775001600 (2026-04-01) à 1782864000 (2026-07-01) ; lecture A : 6, 4, 6 places, N_min 4, modes
        calibre, dernière transaction coinbase pour ETH et USDT ; A-prime : 4, 3, 4 places ; unités 10, 8, 10.
        Mutation : lecture A-prime retenue (rend 4, 3, 4)."""
        p = socle.lire()
        self.assertIsInstance(p, dict)
        self.assertEqual((p["fenetre"]["debut"], p["fenetre"]["fin"]), (1775001600, 1782864000))
        lec = socle.lecture(p)
        self.assertEqual({a: len(v) for a, v in lec["places"].items()}, {"ETH": 6, "USDC": 4, "USDT": 6})
        self.assertEqual((lec["n_min"], set(lec["modes"].values())), ({"ETH": 4, "USDC": 4, "USDT": 4}, {"calibre"}))
        self.assertEqual(lec["derniere_transaction"], {"ETH": ["coinbase"], "USDC": [], "USDT": ["coinbase"]})
        prime = p["lectures"]["A-prime"]["places"]
        self.assertEqual({a: len(v) for a, v in prime.items()}, {"ETH": 4, "USDC": 3, "USDT": 4})
        self.assertEqual([len(p["unites"][a]) for a in socle.ACTIFS], [10, 8, 10])

    def test_parametres_schema(self):
        """Clé en trop, booléen pour un entier, clé absente, accès inconnu, compte d'oracle sans nombre : CA/parametres
        ; flottant et clé dupliquée refusés dès la lecture (illisible). Mutations : schéma retiré ; type non contrôlé ;
        clé en trop admise ; flottant admis ; clé dupliquée admise ; accès non contrôlé ; prédicat de forme ignoré."""
        for modif in (lambda p: p.update(inconnu=1), lambda p: p["passes"].update(A=False), lambda p: p.pop("lot"),
                      lambda p: p["series"]["okx"].update(acces="ftp"),
                      lambda p: p["oracle_sh"]["actives"].append(["USDC", "binance"])):
            self.assertRefus("CA/parametres", socle.lire, ecrire_prm(self, modif))
        for texte in ('{"lot": 0.5}', '{"lot": "x", "lot": "x"}'):
            self.assertIn("illisible", self.assertRefus("CA/parametres", socle.lire, ecrire_prm(self, len, texte)))

    def test_parametres_coherence(self):
        """Place hors des unités, places non triées, N_min au-delà du nombre de places, dernière transaction hors des
        places horodatées, place sans série, planchers seuls pour ETH (F2), lecture inconnue, fenêtre non alignée,
        strates sans le dimanche ; DETTES-T2 : double chevauchement égal au pas (Coinbase), chevauchement hors pages,
        voisins négatifs (OKX) ou hors mensuels (Kraken) : CA/parametres. Mutation : chaque contrôle de cohérence retiré
        à son tour."""
        def a(cle, actif, valeur):
            return lambda p: p["lectures"]["A"][cle].update({actif: valeur})
        cas = [a("places", "USDC", ["binance", "bitfinex", "bitstamp", "kraken", "okx"]),
               a("places", "ETH", ["okx", "kraken", "coinbase", "bitstamp", "bitfinex", "binance"]),
               a("n_min", "USDC", 5), a("derniere_transaction", "USDC", ["binance"]),
               a("places", "USDC", ["binance", "bitfinex", "bitstamp", "gemini", "kraken"]),
               a("modes", "ETH", "planchers_seuls"),
               lambda p: p.update(lecture="B"), lambda p: p["fenetre"].update(debut=1775001601),
               lambda p: p["strates"].update(stress=[5]), lambda p: p["fenetre_descriptive"].update(sans=["okx"]),
               lambda p: p["series"]["coinbase"].update(chevauchement=150),
               lambda p: p["series"]["kraken"].update(chevauchement=1),
               lambda p: p["series"]["okx"].update(voisins=-1), lambda p: p["series"]["kraken"].update(voisins=1)]
        for modif in cas:
            self.assertRefus("CA/parametres", socle.lire, ecrire_prm(self, modif))

    def test_epingle_tau_sigma(self):
        """T-CA-SOC-1 : sha256 du vrai fichier par sha256sum égal à l'épingle, chemin rendu ; copie à un octet altéré
        (dernier octet, bit de poids faible), copie absente : CA/plan-s2bis. Mutation M-CA-01 : contrôle retiré."""
        p = socle.lire()
        chemin = os.path.join(socle.RACINE, p["plan_s2bis"]["tau_sigma"])
        sortie = subprocess.run(["sha256sum", chemin], capture_output=True, text=True, check=True).stdout
        self.assertEqual((sortie.split(" ")[0], socle.tau_sigma(p)), (p["plan_s2bis"]["sha256"], chemin))
        d = tempfile.mkdtemp(prefix="ca_ts_")
        self.addCleanup(shutil.rmtree, d, True)
        self.assertRefus("CA/plan-s2bis", socle.tau_sigma, p, d)
        copie = os.path.join(d, p["plan_s2bis"]["tau_sigma"])
        os.makedirs(os.path.dirname(copie))
        with open(chemin, "rb") as f, open(copie, "wb") as g:
            b = f.read()
            g.write(b[:-1] + bytes([b[-1] ^ 1]))
        self.assertRefus("CA/plan-s2bis", socle.tau_sigma, p, d)

    def test_valeurs_btc(self):
        """Bloc synthétique à la forme de tau_sigma.py l.67-78 : valeurs lues en Decimal ; REFUS, « - » et « aucun »
        sans valeur ; bloc absent, ligne hors forme ou répétée : CA/btc. Mutations : ligne REFUS lue comme valeur ;
        ligne hors forme ignorée."""
        bloc = ["tau agregateur 0.0265", "tau oracle_chainlink REFUS 0.0285 (valeur de la règle, ≥ borne haute exclue "
                "0.0285)", "tau place_horodatee 0.0045", "tau sans_horodatage - (aucune cellule)",
                "sigma agregateur 900", "sigma oracle_chainlink 10800.5", "sigma place_horodatee 90",
                "sigma sans_horodatage aucun"]
        d = tempfile.mkdtemp(prefix="ca_btc_")
        self.addCleanup(shutil.rmtree, d, True)

        def lire(lignes):
            with open(os.path.join(d, "t.txt"), "w", encoding="utf-8") as f:
                f.write(socle.NL.join(["étiquette", "tau x 1", *lignes]) + socle.NL)
            return socle.valeurs_btc(f.name)
        D = socle.Decimal
        self.assertEqual(lire([socle.BLOC, *bloc]), {
            ("tau", "agregateur"): D("0.0265"), ("tau", "place_horodatee"): D("0.0045"),
            ("sigma", "agregateur"): D(900), ("sigma", "oracle_chainlink"): D("10800.5"),
            ("sigma", "place_horodatee"): D(90)})
        for lignes in (bloc, [socle.BLOC, *bloc, "tau agregateur 0.0300"], [socle.BLOC, "tau agregateur 0,0265"],
                       [socle.BLOC, socle.BLOC]):
            self.assertRefus("CA/btc", lire, lignes)


if __name__ == "__main__":
    unittest.main()
