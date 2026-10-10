"""Acquisition II (CA-2 ; E-CA-13) contre le serveur local : pages bornées à la fenêtre, débit par place, point d'entrée
(codes 0, 2, 3, 4). Bornes à la main (date -u -d ; 1775001600 = 2026-04-01 00:00 UTC). Chaque test nomme la mutation
qui le rougit."""
import contextlib
import io
import json
import os
import socket
import subprocess
import sys
import unittest

import acquerir
import tests
import socle
from tests.serveur import Serveur
from tests.test_acquerir import P, local

T0 = 1775001600


def series(prm, base):
    prm["series"]["coinbase"]["url"] = base + "/c/{s}?start={debut_iso}&end={fin_iso}"
    prm["series"]["bitstamp"]["url"] = base + "/s/{s}?n={n}&start={debut}&end={fin}"
    prm["series"]["bitfinex"]["url"] = base + "/f/{s}?start={debut_ms}&end={fin_ms}"


class TestPages(unittest.TestCase):
    def test_pages_bornees(self):
        """700 minutes, DETTES-T2 : Coinbase, 298 minutes utiles + 1 de chaque côté : 23:59-04:58, 04:57-09:56,
        09:55-11:40 UTC ; Bitstamp, une page, n = 702, de 1775001540 à 1775043600 ; Bitfinex en ms, sans chevauchement,
        fin 1775043540 ; Coinbase repris : aucune requête ; deux attentes de 0,34 s. Mutations : borne de page fausse ;
        pas faux ; n faux ; reprise ; débit."""
        fen = {"debut": T0, "fin": T0 + 700 * 60}
        attendus = ["/c/ETH-USD?start=2026-03-31T23:59:00Z&end=2026-04-01T04:58:00Z",
                    "/c/ETH-USD?start=2026-04-01T04:57:00Z&end=2026-04-01T09:56:00Z",
                    "/c/ETH-USD?start=2026-04-01T09:55:00Z&end=2026-04-01T11:40:00Z",
                    "/s/ethusd?n=702&start=1775001540&end=1775043600",
                    "/f/tETHUSD?start=1775001600000&end=1775043540000"]
        horloge, acquerir.HORLOGE = acquerir.HORLOGE, lambda: 100.0
        self.addCleanup(setattr, acquerir, "HORLOGE", horloge)
        with Serveur(dict.fromkeys(attendus, b"[]")) as s:
            prm, d, pauses = local(self, s.base)
            series(prm, s.base)
            for place in ("coinbase", "bitstamp", "bitfinex", "coinbase"):
                acquerir.pages(prm, acquerir.Manifeste(d), "principale", fen, place, "ETH", acquerir.Debit())
        self.assertEqual((s.vus, pauses), (attendus, [0.34, 0.34]))
        self.assertEqual(sorted(os.listdir(os.path.join(d, "principale", "coinbase", "ETH"))),
                         ["page-1775001600.json", "page-1775019480.json", "page-1775037360.json"])

    def test_debit(self):
        """Horloge factice : coinbase à 100 s, 100,1 s, puis bitfinex et coinbase à 100,3 s, intervalle 340 ms :
        attentes de 0,24 s puis 0,14 s, aucune pour bitfinex. Mutations : débit non appliqué ; débit commun aux places ;
        attente pleine, sans le temps écoulé."""
        t = [100.0]
        horloge, acquerir.HORLOGE = acquerir.HORLOGE, lambda: t[0]
        self.addCleanup(setattr, acquerir, "HORLOGE", horloge)
        _prm, _d, pauses = local(self, "http://127.0.0.1:9")
        debit = acquerir.Debit()
        for instant, place in ((100.0, "coinbase"), (100.1, "coinbase"), (100.3, "bitfinex"), (100.3, "coinbase")):
            t[0] = instant
            debit.attendre(place, 340)
        self.assertEqual([round(x, 9) for x in pauses], [0.24, 0.14])

    def test_main(self):
        """Lecture réduite aux places paginées (deux par actif), fenêtres d'une heure et d'une demi-heure : serveur
        muet : code 4, CA/acquisition sur stderr ; puis code 0 et 12 pages au manifeste (reprise) ; variable posée :
        code 3 ; arguments faux : code 2 ; dossier des bruts qui est un fichier : code 4, nommé par le type.
        Mutations : fenêtre descriptive omise ; code de refus faux ; garde non appelée ; exception non nommée."""
        with Serveur({}) as s:
            prm, d, _p = local(self, s.base)
            series(prm, s.base)
            prm["fenetre"].update(fin=T0 + 3600)
            prm["fenetre_descriptive"]["debut"] = 1790811000
            prm["lectures"]["A"].update(places={"ETH": ["bitstamp", "coinbase"], "USDC": ["bitfinex", "bitstamp"],
                                                "USDT": ["bitstamp", "coinbase"]}, n_min=dict.fromkeys(socle.ACTIFS, 2),
                                        derniere_transaction={"ETH": [], "USDC": [], "USDT": []})
            with open(os.path.join(d, "p.json"), "w", encoding="utf-8") as f:
                json.dump(prm, f)
            codes, err = [], io.StringIO()
            with contextlib.redirect_stderr(err):
                for argv, env in ((["--parametres", f.name], {}), (["--parametres", f.name], {}),
                                  (["--parametres", f.name], {"SHOGEN_S2_CAMPAGNE_CONTROL": "x"}), (None, {}),
                                  (["x"], {})):
                    b = ([f.name] if argv == ["x"] else [os.path.join(d, "b")] + argv) if argv is not None else []
                    codes.append(acquerir.main(["--bruts", *b], env))
                    s.defaut = b"[]"
        self.assertEqual((codes, [x.split(" : ")[0] for x in err.getvalue().split(socle.NL)]), (
            [4, 0, 3, 2, 4], ["REFUS CA/acquisition", "REFUS CA/variable", "REFUS CA/usage", "REFUS CA/acquisition",
                              ""]))
        with open(os.path.join(d, "b", "manifeste.tsv"), encoding="utf-8") as f:
            self.assertEqual(len(f.read().split(socle.NL)), 1 + 12 + 1)
        desc = os.path.join(d, "b", "descriptive")                  # C-7 : bornes de la fenêtre descriptive (G08)
        self.assertEqual({x for _r, _s, fs in os.walk(desc) for x in fs}, {"page-1790811000.json"})
        self.assertIn("/s/ethusd?n=32&start=1790810940&end=1790812800", s.vus)    # chevauchement des deux côtés


    def test_garde_reseau(self):
        """Aucune variable de mandataire dans l'environnement des tests ; une URL hors de la boucle locale lève
        ReseauInterdit avant tout envoi (nom non résolu). C-3 : purge vérifiée hors de l'environnement courant, dans un
        sous-processus qui pose quatre variables de mandataire fictives (boucle locale), importe tests et lit
        urllib.request.getproxies() : aucune clé http, https ni all. Mutation G11 : purge retirée (un mandataire sur la
        boucle locale ferait passer la requête), tuée même sans mandataire dans l'environnement du job. Contre-contrôle
        du lot DETTES-T5, passe 2 : getaddrinfo (host=) et getnameinfo hors de la boucle locale refusés et inscrits ;
        mutation : bloc de garde d'avant C-11 (host= et getnameinfo non gardés)."""
        self.assertEqual([k for k in os.environ if k.lower() in ("http_proxy", "https_proxy", "all_proxy")], [])
        with self.assertRaises(tests.ReseauInterdit):
            acquerir.lire_url(local(self, "")[0], "https://example.invalid/x")
        n, levees = len(tests.TENTATIVES), []
        for appel in (lambda: socket.getaddrinfo(host="example.invalid", port=443),
                      lambda: socket.getnameinfo(("192.0.2.1", 80), 0)):
            try:
                appel()
                levees.append(None)
            except BaseException as e:      # ReseauInterdit dérive de BaseException : capture large, bornée au relevé
                levees.append(type(e).__name__)
        self.assertEqual(levees, ["ReseauInterdit"] * 2)
        self.assertEqual([h for _n, h in tests.TENTATIVES[n:]], ["example.invalid", "192.0.2.1"])
        fictif = dict.fromkeys(("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "ALL_PROXY"), "http://127.0.0.1:9")
        code = "import tests, urllib.request as u; print(sorted({'http', 'https', 'all'} & set(u.getproxies())))"
        ici = os.path.dirname(socle.PARAMETRES)
        r = subprocess.run([sys.executable, "-B", "-c", code], cwd=ici, text=True, capture_output=True,
                           env=dict(os.environ, PYTHONPATH=ici, **fictif))
        self.assertEqual((r.returncode, r.stdout), (0, "[]" + socle.NL), r.stderr)


if __name__ == "__main__":
    unittest.main()
