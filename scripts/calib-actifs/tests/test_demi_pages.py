"""Demi-pages redemandées (SHOGEN-CALIB-FORMES-API-1 ; DECISION, ajout daté 17:21:10, C-8 ; lot DETTES-T2) : une page
suspecte de troncature (C-7) est redemandée en deux demi-pages au même débit ; les minutes absentes des deux
demi-réponses sont absentes en vérité ; refus nommé si une demi-réponse est elle-même plafonnée et tronquée. Serveur
local, Coinbase simulée par un plafond de 30 bougies ancré `g` minutes avant start (échangées de start − g à end,
croissantes, les 30 premières), au-delà de la lecture couverte par C-9 (g > 15). Fixture : pas 30, chevauchement 1,
15 créneaux par page (C-9), 13 minutes utiles, 26 minutes en deux pages, couverture simple ; demi-pages à la main :
page 0 (départ −1, borne 13) : [−2 ; 7] et [6 ; 14] ; page 13 (départ 12, borne 26) : [11 ; 20] et [19 ; 27]."""
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
DEMIS = ["2026-03-31T23:58:00Z&end=2026-04-01T00:07:00Z", "2026-04-01T00:06:00Z&end=2026-04-01T00:14:00Z",
         "2026-04-01T00:11:00Z&end=2026-04-01T00:20:00Z", "2026-04-01T00:19:00Z&end=2026-04-01T00:27:00Z"]


def marche(sans):
    return {W0 + 60 * i: (f"{2000 + i}.5", "0" if i in sans else "1") for i in range(-40, 40)}


def plafond(m, g, demis_absentes=False):
    def rendre(chemin):
        q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(chemin).query))
        if demis_absentes and chemin.split("start=")[1] in DEMIS:
            return None                                              # 404 : interruption avant les demi-pages
        a, b = (int(datetime.datetime.strptime(q[k], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc).timestamp()) for k in ("start", "end"))
        if g == "recentes":                                         # les 30 plus récentes avant end (exclu)
            ts = [t for t in sorted(m) if t < b and m[t][1] != "0"][-30:]
        else:
            recul = g if isinstance(g, int) else g.get(q["start"], 20)     # g : minutes, ou par start
            ts = [t for t in sorted(m) if a - 60 * recul <= t <= b and m[t][1] != "0"][:30]
        return ("[" + ", ".join(f"[{t}, 1, 2, 0.5, {m[t][0]}, {m[t][1]}]" for t in ts[::-1]) + "]").encode()
    return rendre


class TestDemiPages(unittest.TestCase):
    def acquis(self, sans, g, panne=False):
        """Deux passages (le premier sans demi-pages si `panne`) ; rend prm, bruts, marché, requêtes par passage, écart
        à la vérité ou refus."""
        m, vus = marche(sans), []
        with Serveur({}) as s:
            prm, d, pauses = local(self, s.base)
            urls(prm, s.base)
            horloge, acquerir.HORLOGE = acquerir.HORLOGE, lambda: 100.0
            self.addCleanup(setattr, acquerir, "HORLOGE", horloge)
            prm["series"]["coinbase"].update(pas=30, chevauchement=1, couverture=1)     # C-8 seul (C-13 : à part)
            prm["reseau"]["essais"] = 1 if panne else 2                     # un seul essai sur la demi-page en panne
            for k in range(2):                                      # second passage : reprise
                s.fonction = plafond(m, g, panne and k == 0)
                essai(lambda: acquerir.pages(prm, acquerir.Manifeste(d), "principale", FEN, "coinbase", "ETH",
                                             acquerir.Debit()))
                vus.append([x.split("start=")[1] for x in s.vus])
                s.vus.clear()
        x = essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", FEN))
        verite = {t: (Decimal(c), True) for t, (c, v) in m.items() if FEN["debut"] <= t < FEN["fin"] and v != "0"}
        self.assertEqual(pauses, [0.34] * sum(max(len(v) - 1, 0) for v in vus))       # même débit pour les demis
        return prm, d, m, vus, (ecart(x, verite) if isinstance(x, dict) else x)

    def test_demi_pages(self):
        """Plafond ancré 20 minutes avant start : chaque page (15 créneaux, 35 bougies servies avant le plafond) est
        tronquée (30 premières : jusqu'à 8 et 21, sous 12 et 25) puis redemandée ; demi-réponses complètes (30 bougies
        jusqu'à 7 ≥ 6, puis 29 ; 30 jusqu'à 20 ≥ 19, puis 29) : série égale à la vérité, 6 requêtes au premier passage,
        aucune au second, 6 fichiers. Minutes 11 et 12 sans échange : absentes des deux demi-réponses, page admise.
        Plafond ancré 40 minutes avant start : demi-réponses plafonnées et tronquées : refus nommé ; de même pour la
        seule seconde demi-page de la page 0 ancrée 25 minutes avant start (30 bougies de −19 à 10, sous 12). Demi-page
        effacée : refus du découpage ; les deux effacées : refus C-7, y compris quand la seule preuve est la
        dernière minute propre (12, page 13 exacte). Mutations : redemande omise ; demi-pages non lues ; demi-page
        non contrôlée ; demi-pages bornées faux ; débit non appliqué ; reprise ignorée ; preuve sans la dernière
        minute."""
        noms = sorted(f"page-{W0 + 780 * k}{x}.json" for k in (0, 1) for x in ("", ".1", ".2"))
        for sans in ((), (11, 12)):
            with self.subTest(sans=sans):
                prm, d, _m, vus, r = self.acquis(sans, 20)
                self.assertEqual((r, len(vus[0]), vus[1], sorted(os.listdir(os.path.join(d, REP))),
                                  [x for x in vus[0] if x in DEMIS]), (([], [], []), 6, [], noms, DEMIS))
                os.remove(os.path.join(d, REP, f"page-{W0}.2.json"))
                trous = [essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", FEN))]
                os.remove(os.path.join(d, REP, f"page-{W0}.1.json"))
                trous.append(essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", FEN)))
                self.assertEqual(trous, [f"REFUS CA/format : {x} ; actif ETH ; place coinbase" for x in (
                    "pages différentes du découpage de la fenêtre",
                    "réponse plafonnée ancrée avant le départ : fin de page tronquée")])
        for g in (40, {"2026-04-01T00:06:00Z": 25}):
            self.assertEqual(self.acquis((), g)[4], "REFUS CA/format : demi-page redemandée plafonnée et tronquée ; "
                                                    "actif ETH ; place coinbase")
        prm, d, _m, _v, r = self.acquis((), {"2026-04-01T00:12:00Z": 0})     # page 13 exacte : seule la minute 12
        for k in (1, 2):                                            # prouve la troncature de la page 0 (9 à 11 perdues)
            os.remove(os.path.join(d, REP, f"page-{W0}.{k}.json"))
        x = essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", FEN))
        self.assertEqual((r, x), (([], [], []), "REFUS CA/format : réponse plafonnée ancrée avant le départ : fin de "
                                                "page tronquée ; actif ETH ; place coinbase"))

    def test_reprise_page_suspecte(self):
        """C-11 (R-2 du contre-contrôle) : premier passage interrompu avant les demi-pages (404 : refus CA/acquisition
        après la page 0) ; second passage : la page 0, déjà acquise et suspecte, est relue et non redemandée, ses deux
        demi-pages le sont, puis la page 13 et les siennes ; 6 fichiers, série égale à la vérité. Mutation X03 : page
        déjà acquise jamais examinée."""
        _prm, d, _m, vus, r = self.acquis((), 20, panne=True)
        self.assertEqual((vus, sorted(os.listdir(os.path.join(d, REP))), r), (
            [["2026-03-31T23:59:00Z&end=2026-04-01T00:13:00Z", DEMIS[0]],
             [DEMIS[0], DEMIS[1], "2026-04-01T00:12:00Z&end=2026-04-01T00:26:00Z", DEMIS[2], DEMIS[3]]],
            sorted(f"page-{W0 + 780 * k}{x}.json" for k in (0, 1) for x in ("", ".1", ".2")), ([], [], [])))

    def test_recentes_sans_preuve(self):
        """C-9 : lecture « les 30 plus récentes jusqu'à end exclu », minutes 6 et 12 sans échange : la page 0 (30
        bougies, une avant le départ, dernière en 11 sous 12) est redemandée ; sa première demi (dernière bougie 5 sous
        m = 6) n'est refusée que sur preuve, et aucun fichier n'a de bougie en ]11 ; 12] ni en ]5 ; 6] : page admise,
        série égale à la vérité, 4 requêtes. Mutation : refus sans preuve (lecture admise refusée)."""
        _prm, d, _m, vus, r = self.acquis((6, 12), "recentes")
        self.assertEqual((r, len(vus[0]), sorted(os.listdir(os.path.join(d, REP)))), (([], [], []), 4, sorted(
            [f"page-{W0}.json", f"page-{W0}.1.json", f"page-{W0}.2.json", f"page-{W0 + 780}.json"])))

    def test_completude_redemandees(self):
        """Ligne de complétude : pages redemandées comptées (2 sur 2, minutes 11 et 12 sans échange : 24 reçues sur
        26). Mutations : compte omis ; compte des demi-pages au lieu des pages."""
        prm, d, _m, _v, _r = self.acquis((11, 12), 20)
        s = essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", FEN))
        self.assertEqual(essai(lambda: tau.completude(prm, "ETH", "principale", FEN, {"coinbase": s}, d)), [
            "[ETH] descriptif : minutes reçues sur attendues, coinbase (principale) : total 24/26 ; pages redemandées "
            "2 ; par page 1775001600 11/13 ; 1775002380 13/13"])


if __name__ == "__main__":
    unittest.main()
