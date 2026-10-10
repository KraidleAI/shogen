"""Formes des API, pages (SHOGEN-CALIB-FORMES-API-1 ; DECISION pts 1 à 3, 5 ; lot DETTES-T2) : acquisition par le code
du lot contre le serveur local, qui simule chaque sémantique de bornes que la place n'écrit pas (Coinbase : début et
fin inclus ou exclus, bougies qui précèdent start, rejet au-delà de `pas` points ; Bitstamp : end prioritaire, fin
incluse ou exclue, ou start prioritaire, début inclus ou exclu, rejet au-delà de `pas` ; Bitfinex : bornes incluses,
tronqué à `pas`), puis chargement : série égale minute pour minute à la vérité. Paramètres de la fixture distincts
d'une place à l'autre (pas 5, 9, 4 ; chevauchement 1, 2, 0), puis ceux du lot."""
import datetime
import json
import os
import unittest
import urllib.parse

import acquerir
import bougies
from tests.serveur import Serveur
from tests.test_acquerir import local
from tests.test_formes import W0, ecart, essai, marche, verite
from tests.test_pages import series as urls

FIXTURE = {"coinbase": (5, 1), "bitstamp": (9, 2), "bitfinex": (4, 0)}             # (pas, chevauchement)


def t_iso(x):
    return int(datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp())


def simule(place, sem, m, pas):
    """Réponse de la place sous `sem` (« debut-exclu », « fin-exclue » ; « avant » : Coinbase rend les `pas` bougies les
    plus récentes jusqu'à la fin, dont celles qui précèdent start, à clôture altérée 9.99 ; « depuis-start » : Bitstamp
    compte `limit` depuis start) ; au-delà de `pas` points : rejet (None, servi en 404) pour Coinbase et Bitstamp,
    troncature pour Bitfinex."""
    def rendre(chemin):
        q, dx, fx = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(chemin).query)), "debut-" in sem, "fin-" in sem
        if place == "coinbase":
            a, b = t_iso(q["start"]), t_iso(q["end"])
            if (b - a) // 60 + 1 - dx - fx > pas:
                return None
            ts = [t for t in sorted(m) if t <= b - 60 * fx and m[t][1] != "0"]
            ts = ts[-pas:] if "avant" in sem else [t for t in ts if t >= a + 60 * dx]
            return ("[" + ", ".join(f"[{t}, 1, 2, 0.5, {m[t][0] if t >= a else '9.99'}, {m[t][1]}]"
                                    for t in ts[::-1]) + "]").encode()
        if place == "bitstamp":                                    # end prioritaire sur start (RAPPORT §2, [lu])
            n, e = int(q["n"]), int(q["end"]) - 60 * fx
            if "depuis-start" in sem:
                e = int(q["start"]) + 60 * dx + 60 * (n - 1)
            ohlc = [{"timestamp": str(t), "close": m[t][0], "volume": m[t][1]}
                    for t in range(e - 60 * n + 60, e + 60, 60)]
            return None if n > pas else json.dumps({"data": {"pair": "ETH/USD", "ohlc": ohlc}}).encode()
        a, b = int(q["start"]) // 1000, int(q["end"]) // 1000      # Bitfinex : MTS >= start et <= end ([lu])
        ts = [t for t in sorted(m) if a <= t <= b and m[t][1] != "0"][:pas]
        return ("[" + ", ".join(f"[{t * 1000}, 1, {m[t][0]}, 2, 0.5, {m[t][1]}]" for t in ts) + "]").encode()
    return rendre


class TestFormesPages(unittest.TestCase):
    def acquis(self, place, sem, fen, fixture):
        m = marche(fen)
        with Serveur({}) as s:
            prm, d, _p = local(self, s.base)
            urls(prm, s.base)
            for p, (pas, ch) in FIXTURE.items() if fixture else ():
                prm["series"][p].update(pas=pas, chevauchement=ch)
            s.fonction = simule(place, sem, m, prm["series"][place]["pas"])

            def f():
                acquerir.pages(prm, acquerir.Manifeste(d), "principale", fen, place, "ETH", acquerir.Debit())
                return bougies.charger(prm, d, "principale", place, "ETH", fen)
            x = essai(f)
        if not isinstance(x, dict):
            return x
        noms = sorted(os.listdir(os.path.join(d, "principale", place, "ETH")))
        return ecart(x, verite(m, fen, place != "bitstamp")), noms

    def test_pages_semantiques(self):
        """Pour chaque place paginée et chaque sémantique : série égale à la vérité (aucune minute manquante, en trop
        ou différente) et pages du découpage, à la main. Fixture, 14 minutes : Coinbase pages en 0, 3, 6, 9, 12 (3
        minutes utiles + 1 de chaque côté), Bitstamp en 0, 5, 10 (5 + 2 + 2), Bitfinex en 0, 4, 8, 12 (sans
        chevauchement). Lot, 1 200 minutes : Coinbase 0, 298, 596, 894, 1192 ; Bitstamp 0, 998 ; Bitfinex une page. Le
        code d'avant perd en silence la dernière minute de chaque page de Coinbase sous « fin exclue », la première
        sous « début exclu » (Q-DT2-1 : la première de la fenêtre avec le seul chevauchement de fin). Mutations :
        chevauchement ignoré ou d'un seul côté ; n faux ; filtre retiré ou à la fenêtre entière ; fenêtre de page non
        bornée à la fenêtre ; doublon identique refusé ; chevauchement ou pas lu à une autre place."""
        cas = [("coinbase", ("incluses", "fin-exclue", "avant", "fin-exclue avant", "debut-exclu",
                             "debut-exclu fin-exclue"), [0, 3, 6, 9, 12, 14], [0, 298, 596, 894, 1192, 1200]),
               ("bitstamp", ("incluses", "fin-exclue", "depuis-start", "depuis-start debut-exclu"), [0, 5, 10, 14],
                [0, 998, 1200]),
               ("bitfinex", ("incluses",), [0, 4, 8, 12, 14], [0, 1200])]
        for place, sems, b_fixture, b_lot in cas:
            for sem in sems:
                for fixture, n, bornes in ((True, 14, b_fixture), (False, 1200, b_lot)):
                    with self.subTest(place=place, sem=sem, fixture=fixture):
                        fen = {"debut": W0, "fin": W0 + 60 * n}
                        pages = [f"page-{W0 + 60 * a}.json" for a in bornes[:-1]]
                        self.assertEqual(self.acquis(place, sem, fen, fixture), (([], [], []), pages))


if __name__ == "__main__":
    unittest.main()
