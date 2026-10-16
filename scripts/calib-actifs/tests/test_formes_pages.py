"""Formes des API, pages (SHOGEN-CALIB-FORMES-API-1 ; DECISION pts 1 à 3, 5 ; lot DETTES-T2) : acquisition par le code
du lot contre le serveur local, qui simule chaque sémantique de bornes que la place n'écrit pas (Coinbase : début et
fin inclus ou exclus, bougies qui précèdent start, rejet au-delà de `pas` points ; Bitstamp : end prioritaire, fin
incluse ou exclue, ou start prioritaire, début inclus ou exclu, rejet au-delà de `pas` ; Bitfinex : bornes incluses,
tronqué à `pas`), puis chargement : série égale minute pour minute à la vérité. Paramètres de la fixture distincts
d'une place à l'autre (pas 10, 18, 8, soit 5, 9 et 4 créneaux par page, C-9 ; chevauchement 1, 2, 0), puis ceux du
lot."""
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

FIXTURE = {"coinbase": (10, 1), "bitstamp": (18, 2), "bitfinex": (8, 0)}             # (pas, chevauchement)


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
            if "tronquee" in sem:                                  # C-7 : plafond ancré pas minutes avant start
                ts = [t for t in sorted(m) if a - 60 * pas <= t <= b and m[t][1] != "0"][:pas]
            return ("[" + ", ".join(f"[{t}, 1, 2, 0.5, {m[t][0] if t >= a else '9.99'}, {m[t][1]}]"
                                    for t in ts[::-1]) + "]").encode()
        if place == "bitstamp":                                    # end prioritaire sur start (RAPPORT §2, [lu])
            n, e = int(q["n"]), int(q["end"]) - 60 * fx
            if "depuis-start" in sem:
                e = int(q["start"]) + 60 * dx + 60 * (n - 1)
            ohlc = [{"timestamp": str(t), "close": m[t][0], "volume": m[t][1]}
                    for t in range(e - 60 * n + 60, e + 60, 60) if t in m]             # C-15 : hors historique, rien
            return None if n > pas else json.dumps({"data": {"pair": "ETH/USD", "ohlc": ohlc}}).encode()
        a, b = int(q["start"]) // 1000, int(q["end"]) // 1000      # Bitfinex : MTS >= start et <= end ([lu])
        ts = [t for t in sorted(m) if a <= t <= b and m[t][1] != "0"][:pas]
        return ("[" + ", ".join(f"[{t * 1000}, 1, {m[t][0]}, 2, 0.5, {m[t][1]}]" for t in ts) + "]").encode()
    return rendre


def echanges(a, b):
    """Minutes échangées de rang a à b exclu (règle de marche, calculée ici)."""
    return sum(i % 7 != 2 for i in range(a, b))


def pages_attendues(bornes, toutes):
    """[(début, reçues, attendues)] des pages de bornes en minutes (à la main)."""
    return [(W0 + 60 * a, b - a if toutes else echanges(a, b), b - a) for a, b in zip(bornes, bornes[1:])]


class TestFormesPages(unittest.TestCase):
    def acquis(self, place, sem, fen, fixture):
        m = marche(fen, marge=1000)              # C-13 : jusqu'à fin + demi-page ; C-15 : historique ≥ 751 minutes
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
        noms = sorted(x for x in os.listdir(os.path.join(d, "principale", place, "ETH")) if not x.startswith("sonde"))
        comptes = essai(lambda: bougies.comptes(prm, place, fen, x))
        return ecart(x, verite(m, fen, place != "bitstamp")), noms, comptes

    def test_pages_semantiques(self):
        """Pour chaque place paginée et chaque sémantique : série égale à la vérité (aucune minute manquante, en trop
        ou différente) et pages du découpage, à la main. Fixture, 14 minutes : Coinbase pages en 0, 3, 6, 9, 12 (3
        minutes utiles + 1 de chaque côté), Bitstamp en 0, 5, 10 (5 + 2 + 2), Bitfinex en 0, 4, 8, 12 (sans
        chevauchement). Lot, 1 200 minutes, C-9 : Coinbase par 148, Bitstamp 0, 498, 996 ; Bitfinex une page. Le
        code d'avant perd en silence la dernière minute de chaque page de Coinbase sous « fin exclue », la première
        sous « début exclu » (Q-DT2-1 : la première de la fenêtre avec le seul chevauchement de fin). Mutations :
        chevauchement ignoré ou d'un seul côté ; n faux ; filtre retiré ou à la fenêtre entière ; fenêtre de page non
        bornée à la fenêtre ; doublon identique refusé ; chevauchement ou pas lu à une autre place.
        Comptes par page (DECISION pt 5) : reçues et attendues à la main (règle du marché) ; mutations : attendues ou
        reçues fausses, dernière page mal bornée. C-7 et C-8 : « fin exclue, avant » (plafond ancré avant le départ,
        sans la dernière minute propre, sans échange : minute 2 de la fixture, 443 et 1199 du lot) : page redemandée en
        deux demi-pages, admise ; plafond ancré `pas` minutes avant start : demi-réponses elles aussi tronquées : refus
        nommé ; mutations : contrôle retiré, plafond ignoré. C-13 : Coinbase et Bitstamp en couverture double, second
        découpage à la main (fixture : Coinbase −1 à 14 par 3, Bitstamp −2 à 13 par 5 ; lot : Coinbase −74 à 1258 par
        148, Bitstamp −249 à 1245 par 498), double 14 et 814 redemandées sous « fin exclue, avant » (dernières minutes
        16 et 961 sans échange) ; refus « tronquee » nommé par le second découpage, contrôlé le premier."""
        cas = [("coinbase", ("incluses", "fin-exclue", "avant", "fin-exclue avant", "debut-exclu",
                             "debut-exclu fin-exclue", "tronquee"), [0, 3, 6, 9, 12, 14],
                [0, 148, 296, 444, 592, 740, 888, 1036, 1184, 1200], [-1, 2, 5, 8, 11, 14], range(-74, 1274, 148)),
               ("bitstamp", ("incluses", "fin-exclue", "depuis-start", "depuis-start debut-exclu"), [0, 5, 10, 14],
                [0, 498, 996, 1200], [-2, 3, 8, 13], [-249, 249, 747, 1245]),
               ("bitfinex", ("incluses",), [0, 4, 8, 12, 14], [0, 1200], [], [])]
        tronque = "REFUS CA/format : couverture double discordante ; actif ETH ; place coinbase"
        for place, sems, b_fixture, b_lot, d_fixture, d_lot in cas:
            for sem in sems:
                for fixture, n, bornes, dbl in ((True, 14, b_fixture, d_fixture), (False, 1200, b_lot, d_lot)):
                    with self.subTest(place=place, sem=sem, fixture=fixture):
                        fen = {"debut": W0, "fin": W0 + 60 * n}
                        pages = sorted([f"page-{W0 + 60 * a}.json" for a in bornes[:-1]]
                                       + [f"double-{W0 + 60 * a}.json" for a in dbl])
                        if sem == "fin-exclue avant":   # C-8 : page 0 et double 14 (fixture), 296, 1184, double 814
                            pages = sorted(pages + [f"{x}-{W0 + 60 * a}.{k}.json" for x, a in (
                                (("page", 0), ("double", 14)) if fixture else (("page", 296), ("page", 1184),
                                                                              ("double", 814))) for k in (1, 2)])
                        attendu = (([], [], []), pages, pages_attendues(bornes, place == "bitstamp"))
                        obtenu = self.acquis(place, sem, fen, fixture)
                        self.assertEqual(obtenu, tronque if sem == "tronquee" else attendu)


if __name__ == "__main__":
    unittest.main()
