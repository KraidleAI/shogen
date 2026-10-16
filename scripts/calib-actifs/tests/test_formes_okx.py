"""Formes des API, mensuels d'OKX (SHOGEN-CALIB-FORMES-API-1 ; DECISION pt 4 ; lot DETTES-T2) : mensuels alignés en
UTC, UTC+8 ou UTC-4, servis par le serveur local ; voisins 1 pour OKX, 0 pour Binance (valeurs distinctes). Bornes à
la main (date -u -d : 1780272000 = 2026-06-01 00:00 UTC ; 1782842400 = 2026-06-30 18:00)."""
import io
import os
import unittest
import zipfile

import acquerir
import bougies
from tests.serveur import Serveur
from tests.test_acquerir import P, local
from tests.test_formes import NL, ecart, essai, marche, verite


def okx_mensuels(m, decalage_h):
    """Mensuels synthétiques 2026-05 à 07 d'OKX, chacun de [début du mois - décalage ; début du suivant - décalage)."""
    debuts, f = (1777593600, 1780272000, 1782864000, 1785542400), {}
    for mois, a, b in zip(("2026-05", "2026-06", "2026-07"), debuts, debuts[1:]):
        lignes = [f"ETH-USDT,1,2,0.5,{c},{v},0,0,{t * 1000},1" for t, (c, v) in sorted(m.items())
                  if a - 3600 * decalage_h <= t < b - 3600 * decalage_h]
        b_ = io.BytesIO()
        with zipfile.ZipFile(b_, "w") as z:
            z.writestr("m.csv", NL.join(["instrument_name,open,high,low,close,vol,vol_ccy,vol_quote,open_time,confirm",
                                         *lignes]) + NL)
        f[f"/o/{mois.replace('-', '')}/ETH-USDT-{mois}.zip"] = b_.getvalue()
    return f


class TestFormesOkx(unittest.TestCase):
    def test_okx_mois_voisins(self):
        """DECISION pt 4 : mensuels d'OKX alignés en UTC, UTC+8 (indice du RAPPORT §4a) ou UTC-4 ; fenêtres de six
        heures au début de juin (1780272000 à 1780293600) et à la fin (1782842400 à 1782864000) : mois 2026-05, 06
        et 07 demandés (voisins 1), minutes hors fenêtre écartées, série égale à la vérité ; mois(fenêtre, 1) : 2026-03
        à 07 pour la fenêtre du lot, 08 à 10 pour septembre, 2026-11 à 2027-02 au passage d'année. Binance (voisins 0)
        reste strict : minute hors fenêtre : CA/format. Mutations : voisins non acquis ; mois précédent ou suivant
        seul ; filtre d'OKX retiré ; voisins lus à une autre place ; Binance filtré."""
        for decalage in (0, 8, -4):
            for fen in ({"debut": 1780272000, "fin": 1780293600}, {"debut": 1782842400, "fin": 1782864000}):
                m = marche(fen, k=5, marge=720)
                with self.subTest(decalage=decalage, debut=fen["debut"]), Serveur(okx_mensuels(m, decalage)) as s:
                    prm, d, _p = local(self, s.base)
                    prm["series"]["okx"]["voisins"], prm["series"]["binance"]["voisins"] = 1, 0

                    def f():
                        acquerir.mensuels(prm, acquerir.Manifeste(d), "principale", fen, "okx", "ETH")
                        return ecart(bougies.charger(prm, d, "principale", "okx", "ETH", fen), verite(m, fen, False))
                    self.assertEqual((essai(f), s.vus), (([], [], []), [
                        f"/o/2026{i:02d}/ETH-USDT-2026-{i:02d}.zip" for i in (5, 6, 7)]))
        os.makedirs(os.path.join(d, "principale", "binance", "ETH"))
        with zipfile.ZipFile(os.path.join(d, "principale", "binance", "ETH", "b.zip"), "w") as z:
            z.writestr("m.csv", "".join(f"{t * 10 ** 6},1,2,0.5,1.5,1,0,0,0,0,0,0{NL}"
                                        for t in range(fen["debut"], fen["fin"] + 60, 60)))
        self.assertEqual(essai(lambda: bougies.charger(prm, d, "principale", "binance", "ETH", fen)),
                         "REFUS CA/format : temps hors fenêtre ou hors minute ; actif ETH ; place binance")
        annee = {"debut": 1798758000, "fin": 1798765200}
        self.assertEqual(essai(lambda: [acquerir.mois(f, 1) for f in (P["fenetre"], P["fenetre_descriptive"], annee)]),
                         [[f"2026-0{i}" for i in range(3, 8)], ["2026-08", "2026-09", "2026-10"],
                          ["2026-11", "2026-12", "2027-01", "2027-02"]])

    def test_okx_garde_et_mois_absent(self):
        """C-1 de la G2 : fenêtre de fin de juin, voisins 1 : garde des mois acquis [2026-05-01 − 14 h ; 2026-08-01
        + 14 h) = [1777543200 ; 1785592800) (date -u -d) ; minutes 1777543200 et 1785592740 écartées sans refus ;
        1777543140, 1785592800, 2025-01-01 (1735689600) et un mensuel en microsecondes : refus CA/format. C-2 :
        septembre sans le mensuel 2026-10 : refus nommé (mois, motif, actif, place). Mutations : garde retirée ; garde
        décalée d'une minute ; refus du mensuel absent non nommé."""
        fen = {"debut": 1782842400, "fin": 1782864000}
        m = marche(fen, k=5, marge=0)
        refus = "REFUS CA/format : temps hors fenêtre ou hors minute ; actif ETH ; place okx"
        for k, (hors, unite, attendu) in enumerate(((1777543200, 1000, ([], [], [])), (1785592740, 1000, ([], [], [])),
                                                    (1777543140, 1000, refus), (1785592800, 1000, refus),
                                                    (1735689600, 1000, refus), (None, 10 ** 6, refus))):
            with self.subTest(cas=k):
                prm, d, _p = local(self, "http://127.0.0.1:9")
                prm["series"]["okx"]["voisins"] = 1
                os.makedirs(os.path.join(d, "principale", "okx", "ETH"))
                lignes = [f"ETH-USDT,1,2,0.5,{c},{v},0,0,{t * unite},1" for t, (c, v) in sorted(m.items())]
                with zipfile.ZipFile(os.path.join(d, "principale", "okx", "ETH", "m.zip"), "w") as z:
                    entete = "instrument_name,open,high,low,close,vol,vol_ccy,vol_quote,open_time,confirm"
                    plus = [f"X,1,1,1,1,1,0,0,{hors * 1000},1"] if hors else []
                    z.writestr("m.csv", NL.join([entete, *lignes, *plus]) + NL)
                x = essai(lambda: bougies.charger(prm, d, "principale", "okx", "ETH", fen))
                self.assertEqual(ecart(x, verite(m, fen, False)) if isinstance(x, dict) else x, attendu)
        with Serveur({f"/o/2026{i}/ETH-USDT-2026-{i}.zip": b"x" for i in ("08", "09")}) as s:
            prm, d, _p = local(self, s.base)
            self.assertEqual(essai(lambda: acquerir.mensuels(prm, acquerir.Manifeste(d), "descriptive",
                                                             P["fenetre_descriptive"], "okx", "ETH")),
                             "REFUS CA/acquisition : mensuel 2026-10 non obtenu (téléchargement impossible "
                             "(HTTPError)) ; un mensuel n'est publié qu'après la fin de son mois ; actif ETH ; "
                             "place okx")


if __name__ == "__main__":
    unittest.main()
