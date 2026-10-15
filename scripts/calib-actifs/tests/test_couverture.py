"""Double couverture (SHOGEN-CALIB-FORMES-API-1 ; DECISION, ajout daté 19:48:33, C-13 et C-14 ; lot DETTES-T2) : deux
requêtes d'ancrages différents par minute (découpage de C-9 et second décalé d'une demi-page) ; minute présente dans
une réponse et absente d'une autre qui la couvre, ou aux valeurs différentes : refus nommé. Serveur local, Coinbase,
pas 30, chevauchement 1 : 15 créneaux, 13 minutes utiles, demi-page 6. Fenêtre de 40 minutes, à la main : pages 0,
13, 26, 39 (requêtes [début − 1 ; fin]) ; second découpage −6, 7, 20, 33 (jusqu'à fin + 6 au moins), double-<début>."""
import datetime
import os
import unittest
import urllib.parse
from decimal import Decimal

import acquerir
import bougies
from tests.serveur import Serveur
from tests.test_acquerir import local
from tests.test_formes import W0, ecart, essai
from tests.test_pages import series as urls

FEN = {"debut": W0, "fin": W0 + 40 * 60}
REP = os.path.join("principale", "coinbase", "ETH")
DISCORDE = "REFUS CA/format : couverture double discordante ; actif ETH ; place coinbase"


def lecture(m, mode, g=0, faux=None, vues=None):
    """Bougies échangées de m servies selon le mode : exact [s ; e] ; recentes, les 30 plus récentes avant e exclu ;
    cpt, les 30 premières de [s − g ; e] ; cren, [s − g ; e − g] (fenêtre décalée) ; crenp, [s − g ; s − g + 29] ∩
    [.. ; e]. `faux` : clôture fausse à cette minute (rang depuis W0) dans les réponses du second découpage (requêtes
    de départ ≡ 6 modulo 13 minutes). Requêtes (s, e) notées dans `vues`."""
    def rendre(chemin):
        q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(chemin).query))
        a, b = (int(datetime.datetime.strptime(q[k], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc).timestamp()) for k in ("start", "end"))
        if vues is not None:
            vues.append((a, b))
        tr, r = [t for t in sorted(m) if m[t][1] != "0"], 60 * g
        ts = {"exact": [t for t in tr if a <= t <= b], "recentes": [t for t in tr if t < b][-30:],
              "cpt": [t for t in tr if a - r <= t <= b][:30], "cren": [t for t in tr if a - r <= t <= b - r],
              "crenp": [t for t in tr if a - r <= t <= min(b, a - r + 29 * 60)]}[mode]
        double = (a - W0) // 60 % 13 == 6
        cl = {t: ("9.5" if double and faux is not None and t == W0 + 60 * faux else m[t][0]) for t in ts}
        return ("[" + ", ".join(f"[{t}, 1, 2, 0.5, {cl[t]}, {m[t][1]}]" for t in ts[::-1]) + "]").encode()
    return rendre


class TestCouverture(unittest.TestCase):
    def acquis(self, fen, serveur, **serie):
        """Deux passages (le second : reprise) ; rend (requêtes par passage, fichiers, écart à la vérité ou refus).
        Échanges des minutes `historique` (−200 par défaut) à `fin` (200) exclue ; sondes (C-15) depuis W0 − 999."""
        m, vus = {W0 + 60 * i: (f"{2000 + i}.5", "1")
                  for i in range(serie.pop("historique", -200), serie.pop("fin", 200))}, []
        m.update({W0 + 60 * i: ("1.5", "0") for i in serie.pop("sans", ())})
        with Serveur({}) as s:
            prm, d, pauses = local(self, s.base)
            urls(prm, s.base)
            horloge, acquerir.HORLOGE = acquerir.HORLOGE, lambda: 100.0
            self.addCleanup(setattr, acquerir, "HORLOGE", horloge)
            prm["series"]["coinbase"].update(serie)
            prm["historique"] = {"debut": W0 - 999 * 60, "source": "tests"}
            s.fonction = serveur(m)
            for _k in range(2):
                essai(lambda: acquerir.pages(prm, acquerir.Manifeste(d), "principale", fen, "coinbase", "ETH",
                                             acquerir.Debit()))
                vus.append(len(s.vus))
                s.vus.clear()
        x = essai(lambda: bougies.charger(prm, d, "principale", "coinbase", "ETH", fen))
        verite = {t: (Decimal(c), True) for t, (c, v) in m.items() if fen["debut"] <= t < fen["fin"] and v != "0"}
        self.assertEqual(pauses, [0.34] * max(vus[0] - 1, 0))                   # même débit, un seul passage
        self.bruts = prm, d
        return vus, sorted(os.listdir(os.path.join(d, REP))), (ecart(x, verite) if isinstance(x, dict) else x)

    def test_double_couverture(self):
        """Lecture exacte, « 30 plus récentes » (minutes 11 et 12 sans échange), fenêtre décalée d'une minute
        (absorbée par le chevauchement) : série égale à la vérité ; lecture exacte : 8 requêtes, aucune à la reprise,
        fichiers page-0, 13, 26, 39 et double-−6, 7, 20, 33, et 11 sondes (C-15, à la main : 25, −487, −231, −103, −167,
        −199, −215, −207, −211, −213, −214 ; première bougie en −200). Fenêtre décalée de 2 minutes (la page 0 du second
        découpage perd la minute 6, servie par la page 0 du premier) ; plafond de 30 bougies ou de 30 créneaux ancré
        100 minutes avant start (toute réponse avant son départ) ; clôture différente à la minute 10 dans le second
        découpage : refus nommé. Mutations : second découpage omis ; non décalé ; non chargé ; contrôle de couverture
        retiré ; valeurs non comparées ; bougies d'avant le départ non comptées comme preuve."""
        noms = sorted([f"{x}-{W0 + d + 780 * k}.json" for x, d in (("page", 0), ("double", -360)) for k in range(4)] + [
            f"sonde-{W0 + 60 * x}.json" for x in (25, -487, -231, -103, -167, -199, -215, -207, -211, -213, -214)])
        cas = {"exact": lambda m: lecture(m, "exact"), "recentes": lambda m: lecture(m, "recentes"),
               "cren-1": lambda m: lecture(m, "cren", 1)}
        for nom, f in cas.items():
            with self.subTest(nom=nom):
                vus, fichiers, r = self.acquis(FEN, f, pas=30, chevauchement=1, couverture=2,
                                               sans=(11, 12) if nom == "recentes" else ())
                self.assertEqual(r, ([], [], []))
                if nom == "exact":
                    self.assertEqual((vus, fichiers), ([19, 0], noms))
        cas = {"cren-2": lambda m: lecture(m, "cren", 2), "cpt-100": lambda m: lecture(m, "cpt", 100),
               "crenp-100": lambda m: lecture(m, "crenp", 100), "faux": lambda m: lecture(m, "exact", faux=10)}
        for nom, f in cas.items():
            with self.subTest(nom=nom):
                self.assertEqual(self.acquis(FEN, f, pas=30, chevauchement=1, couverture=2)[2], DISCORDE)

    def test_aucune_demi_requete_vide(self):
        """C-14 : couverture simple, chevauchement 0, pas 30 (15 minutes utiles), fenêtre de 16 minutes : pages 0 et 15
        (un seul point) ; plafond de 30 bougies ancré 40 minutes avant start : les deux réponses sont suspectes ; la
        page 0 est redemandée en deux moitiés, la page d'un point ne l'est pas ; aucune requête de départ après sa fin.
        Mutation : demi-pages d'une page d'un point."""
        vues = []
        _v, fichiers, _r = self.acquis({"debut": W0, "fin": W0 + 960}, lambda m: lecture(m, "cpt", 40, vues=vues),
                                       pas=30, chevauchement=0, couverture=1)
        self.assertEqual(([x for x in vues if x[0] > x[1]], fichiers), ([], sorted(
            [f"page-{W0}.json", f"page-{W0}.1.json", f"page-{W0}.2.json", f"page-{W0 + 900}.json"])))


if __name__ == "__main__":
    unittest.main()
