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
        """700 minutes, DETTES-T2 et C-9 (créneaux ≤ pas / 2) : Coinbase, 148 minutes utiles + 1 de chaque côté :
        23:59-02:28, 02:27-04:56, 04:55-07:24, 07:23-09:52, 09:51-11:40 UTC ; Bitstamp, 498 minutes utiles : n = 500 de
        1775001540 à 1775031480, puis n = 204 de 1775031420 à 1775043600 ; Bitfinex en ms, une page, fin 1775043540 ;
        C-13, second découpage décalé d'une demi-page jusqu'à fin + demi-page : Coinbase (74 minutes) 22:45-01:14 (le
        31), 01:13-03:42, 03:41-06:10, 06:09-08:38, 08:37-11:06, 11:05-13:34 ; Bitstamp (249 minutes) n = 500 depuis
        1774986600, 1775016480 et 1775046360 ; C-15, sondes vides en recul depuis fin − ⌊pas/2⌋ jusqu'au début de
        l'historique fixé à −300 minutes (Coinbase : 550, 400, 100, −300 ; Bitstamp n = 500 : 200, −300) ; Coinbase
        repris : aucune requête ; attentes : 14 de 0,34 s, 6 de 0,2 s.
        Mutations : borne de page fausse ; pas faux ; n faux ; reprise ; débit ; second découpage omis ou mal décalé."""
        fen = {"debut": T0, "fin": T0 + 700 * 60}
        attendus = [f"/c/ETH-USD?start=2026-0{a}:00Z&end=2026-0{b}:00Z" for a, b in (
            ("3-31T23:59", "4-01T02:28"), ("4-01T02:27", "4-01T04:56"), ("4-01T04:55", "4-01T07:24"),
            ("4-01T07:23", "4-01T09:52"), ("4-01T09:51", "4-01T11:40"), ("3-31T22:45", "4-01T01:14"),
            ("4-01T01:13", "4-01T03:42"), ("4-01T03:41", "4-01T06:10"), ("4-01T06:09", "4-01T08:38"),
            ("4-01T08:37", "4-01T11:06"), ("4-01T11:05", "4-01T13:34"), ("4-01T09:10", "4-01T11:39"),
            ("4-01T06:40", "4-01T09:09"), ("4-01T01:40", "4-01T04:09"), ("3-31T19:00", "3-31T21:29"))] + [
            "/s/ethusd?n=500&start=1775001540&end=1775031480", "/s/ethusd?n=204&start=1775031420&end=1775043600"] + [
            f"/s/ethusd?n=500&start={a}&end={a + 29940}" for a in (1774986600, 1775016480, 1775046360, 1775013600,
                                                                    1774983600)] + [
            "/f/tETHUSD?start=1775001600000&end=1775043540000"]
        horloge, acquerir.HORLOGE = acquerir.HORLOGE, lambda: 100.0
        self.addCleanup(setattr, acquerir, "HORLOGE", horloge)
        with Serveur(dict.fromkeys(attendus, b"[]")) as s:
            prm, d, pauses = local(self, s.base)
            series(prm, s.base)
            prm["historique"]["debut"] = T0 - 18000
            for place in ("coinbase", "bitstamp", "bitfinex", "coinbase"):
                acquerir.pages(prm, acquerir.Manifeste(d), "principale", fen, place, "ETH", acquerir.Debit())
        self.assertEqual((s.vus, pauses), (attendus, [0.34] * 14 + [0.2] * 6))
        self.assertEqual(sorted(os.listdir(os.path.join(d, "principale", "coinbase", "ETH"))), sorted(
            [f"page-{x}.json" for x in (1775001600, 1775010480, 1775019360, 1775028240, 1775037120)]
            + [f"double-{1775001600 + 60 * x}.json" for x in (-74, 74, 222, 370, 518, 666)]
            + [f"sonde-{1775001600 + 60 * x}.json" for x in (550, 400, 100, -300)]))

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
        muet : code 4, CA/acquisition sur stderr ; puis code 0 et 98 fichiers au manifeste (reprise ; 12 du premier
        découpage, 2 du second par fenêtre et par paire de Coinbase et de Bitstamp, C-13 ; sondes vides en recul jusqu'à
        l'historique fixé à −300 minutes, C-15 : principale 3 par paire de Coinbase, 1 de Bitstamp ; descriptive 12 et
        11, en haut − k (2^j − 1), calculées ici) ; variable posée :
        code 3 ; arguments faux : code 2 ; dossier des bruts qui est un fichier : code 4, nommé par le type.
        Mutations : fenêtre descriptive omise ; code de refus faux ; garde non appelée ; exception non nommée."""
        with Serveur({}) as s:
            prm, d, _p = local(self, s.base)
            series(prm, s.base)
            prm["fenetre"].update(fin=T0 + 3600)
            prm["fenetre_descriptive"]["debut"] = 1790811000
            prm["historique"]["debut"] = T0 - 18000
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
            self.assertEqual(len(f.read().split(socle.NL)), 1 + 98 + 1)
        desc = os.path.join(d, "b", "descriptive")                  # C-7 : bornes de la fenêtre descriptive (G08)
        self.assertEqual({x for _r, _s, fs in os.walk(desc) for x in fs}, {"page-1790811000.json"} | {
            f"double-{1790811000 + h}.json" for h in (-4440, 4440, -14940, 14940)} | {
            f"sonde-{max(T0 - 18000, haut - k * (2 ** j - 1))}.json" for haut, k, n in (
                (1790803800, 9000, 12), (1790782800, 30000, 11)) for j in range(n)})
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
