"""Demi-pages redemandées (SHOGEN-CALIB-FORMES-API-1 ; DECISION, ajout daté 17:21:10, C-8 ; lot DETTES-T2) : une page
suspecte de troncature (C-7) est redemandée en deux demi-pages au même débit ; les minutes absentes des deux
demi-réponses sont absentes en vérité ; refus nommé si une demi-réponse est elle-même plafonnée et tronquée. Serveur
local, Coinbase simulée par un plafond ancré `g` minutes avant start (bougies échangées de start − g à end, croissantes,
les `pas` premières). Fixture : pas 15, chevauchement 1 (13 minutes utiles), 26 minutes en deux pages ; demi-pages à la
main : page 0 (départ −1, borne 13) : [−2 ; 7] et [6 ; 14] ; page 13 (départ 12, borne 26) : [11 ; 20] et [19 ; 27]."""
import datetime
import os
import unittest
import urllib.parse
from decimal import Decimal

import acquerir
import bougies
import tau
from tests.serveur import Serveur
from tests.test_acquerir import local
from tests.test_formes import W0, ecart, essai
from tests.test_pages import series as urls

FEN = {"debut": W0, "fin": W0 + 26 * 60}
REP = os.path.join("principale", "coinbase", "ETH")


def marche(sans):
    return {W0 + 60 * i: (f"{2000 + i}.5", "0" if i in sans else "1") for i in range(-40, 40)}


def plafond(m, g):
    def rendre(chemin):
        q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(chemin).query))
        a, b = (int(datetime.datetime.strptime(q[k], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc).timestamp()) for k in ("start", "end"))
        recul = g if isinstance(g, int) else g.get(q["start"], 4)          # g : minutes, ou par start
        ts = [t for t in sorted(m) if a - 60 * recul <= t <= b and m[t][1] != "0"][:15]
        return ("[" + ", ".join(f"[{t}, 1, 2, 0.5, {m[t][0]}, {m[t][1]}]" for t in ts[::-1]) + "]").encode()
    return rendre


class TestDemiPages(unittest.TestCase):
    def acquis(self, sans, g):
        m = marche(sans)
        with Serveur({}) as s:
            prm, d, pauses = local(self, s.base)
            urls(prm, s.base)
            horloge, acquerir.HORLOGE = acquerir.HORLOGE, lambda: 100.0
            self.addCleanup(setattr, acquerir, "HORLOGE", horloge)
            prm["series"]["coinbase"].update(pas=15, chevauchement=1)
            s.fonction = plafond(m, g)
            for _ in range(2):                                      # second passage : reprise, aucune requête neuve
                essai(lambda: acquerir.pages(prm, acquerir.Manifeste(d), "principale", FEN, "coinbase", "ETH",
                                             acquerir.Debit()))
        x = essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", FEN))
        verite = {t: (Decimal(c), True) for t, (c, v) in m.items() if FEN["debut"] <= t < FEN["fin"] and v != "0"}
        self.assertEqual(pauses, [0.34] * (len(s.vus) - 1))                # même débit pour les demi-pages
        return prm, d, m, s.vus, (ecart(x, verite) if isinstance(x, dict) else x)

    def test_demi_pages(self):
        """Plafond ancré 4 minutes avant start : chaque page (15 bougies demandées, 19 servies avant le plafond) est
        tronquée (dernières 15 : jusqu'à 9 et 22, sous 12 et 25) puis redemandée ; demi-réponses sous le plafond (14 et
        13 bougies) : série égale à la vérité, 6 requêtes au premier passage, aucune au second, 6 fichiers. Minutes 11
        et 12 sans échange : absentes des deux demi-réponses, page admise. Plafond ancré 15 minutes avant start : les
        demi-réponses sont elles-mêmes plafonnées et tronquées : refus nommé ; de même pour la seule seconde
        demi-page de la page 0 ancrée 10 minutes avant start (minutes 11 et 12 perdues sinon). Demi-page effacée :
        refus du découpage ; les deux effacées : refus C-7. Mutations : redemande omise ; demi-pages non lues ;
        demi-page non contrôlée ; demi-pages bornées faux ; débit non appliqué ; reprise des demi-pages ignorée."""
        noms = sorted(f"page-{W0 + 780 * k}{x}.json" for k in (0, 1) for x in ("", ".1", ".2"))
        demis = ["2026-03-31T23:58:00Z&end=2026-04-01T00:07:00Z", "2026-04-01T00:06:00Z&end=2026-04-01T00:14:00Z",
                 "2026-04-01T00:11:00Z&end=2026-04-01T00:20:00Z", "2026-04-01T00:19:00Z&end=2026-04-01T00:27:00Z"]
        for sans in ((), (11, 12)):
            with self.subTest(sans=sans):
                prm, d, _m, vus, r = self.acquis(sans, 4)
                self.assertEqual((r, len(vus), sorted(os.listdir(os.path.join(d, REP))),
                                  [x.split("start=")[1] for x in vus if x.split("start=")[1] in demis]),
                                 (([], [], []), 6, noms, demis))
                os.remove(os.path.join(d, REP, f"page-{W0}.2.json"))
                trous = [essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", FEN))]
                os.remove(os.path.join(d, REP, f"page-{W0}.1.json"))
                trous.append(essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", FEN)))
                self.assertEqual(trous, [f"REFUS CA/format : {x} ; actif ETH ; place coinbase" for x in (
                    "pages différentes du découpage de la fenêtre",
                    "réponse plafonnée ancrée avant le départ : fin de page tronquée")])
        for g in (15, {"2026-04-01T00:06:00Z": 10}):     # seconde demi seule tronquée : 15 bougies de −4 à 10, sous 12
            self.assertEqual(self.acquis((), g)[4], "REFUS CA/format : demi-page redemandée plafonnée et tronquée ; "
                                                    "actif ETH ; place coinbase")

    def test_completude_redemandees(self):
        """Ligne de complétude : pages redemandées comptées (2 sur 2, minutes 11 et 12 sans échange : 24 reçues sur
        26). Mutations : compte omis ; compte des demi-pages au lieu des pages."""
        prm, d, _m, _v, _r = self.acquis((11, 12), 4)
        s = essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", FEN))
        self.assertEqual(essai(lambda: tau.completude(prm, "ETH", "principale", FEN, {"coinbase": s}, d)), [
            "[ETH] descriptif : minutes reçues sur attendues, coinbase (principale) : total 24/26 ; pages redemandées "
            "2 ; par page 1775001600 11/13 ; 1775002380 13/13"])


if __name__ == "__main__":
    unittest.main()
