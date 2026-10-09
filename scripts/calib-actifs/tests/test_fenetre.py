"""Fenêtre et strates (T-CA-FEN-1), planchers des oracles (T-CA-ORA-1), écriture des sorties (E-CA-04, E-CA-05).
Instants par date -u -d ; planchers à la main (1,5 × 0,5 % ; 1,5 × 0,25 % ; 1,5 × 3 600, 82 800, 86 400) et contre
config_analyse.py l.28-29 (lu, jamais modifié). Chaque test nomme la mutation qui le rougit."""
import os
import shutil
import sys
import tempfile
import time
import unittest
from decimal import Decimal

import socle

sys.path.insert(0, os.path.join(socle.RACINE, "s2bis"))
from shogen_s2bis.recalc import config_analyse  # noqa: E402

P = socle.lire()


class TestFenetre(unittest.TestCase):
    def setUp(self):
        """Fuseau local à UTC+14 le temps du test : une strate lue en heure locale change de jour."""
        avant = os.environ.get("TZ")
        os.environ["TZ"] = "Pacific/Kiritimati"
        time.tzset()
        self.addCleanup(lambda: (os.environ.pop("TZ") if avant is None else os.environ.update(TZ=avant), time.tzset()))

    def test_fenetre_et_strates(self):
        """T-CA-FEN-1 : 131 040 minutes de 1775001600 (mercredi 2026-04-01) inclus à 1782864000 exclu ; 37 440 en
        stress, 93 600 en calme ; samedi 1775260800 stress, lundi 1775433600 calme, vendredi 23:59 UTC (1775260740)
        calme, dimanche 23:59 UTC (1775433540) stress. Mutations M-CA-03 : jour pris en heure locale ; M-CA-04 : borne
        haute incluse."""
        m = socle.minutes(P["fenetre"])
        self.assertEqual((len(m), m[0], m[-1]), (131040, 1775001600, 1782864000 - 60))
        stress = sum(socle.strate(t, P) == "stress" for t in m)
        self.assertEqual((stress, len(m) - stress), (37440, 93600))
        self.assertEqual([socle.strate(t, P) for t in (1775260800, 1775433600, 1775260740, 1775433540)],
                         ["stress", "calme", "calme", "stress"])

    def test_oracles(self):
        """T-CA-ORA-1 : 0,0075 et 0,00375 (hors grille de 0,0005, admis) ; 5 400, 124 200, 129 600 s ; égaux à
        TAU_ORACLES et SIGMA_ORACLES de config_analyse ; seuil relu différent : CA/chainlink. Mutation M-CA-16 :
        plancher arrondi à la grille (0,0040)."""
        o = socle.oracles(P)
        self.assertEqual(o, {"ETH": (Decimal("0.0075"), 5400), "USDC": (Decimal("0.00375"), 124200),
                             "USDT": (Decimal("0.00375"), 129600)})
        self.assertEqual({a: str(t) for a, (t, _s) in o.items()}, config_analyse.TAU_ORACLES)
        self.assertEqual({a: o[a][1] for a in config_analyse.SIGMA_ORACLES}, config_analyse.SIGMA_ORACLES)
        for cle, valeur in (("heartbeat_s", 82800), ("seuil", "0.003")):           # C-9 : seuil, mutation G12
            q = socle.json.loads(socle.json.dumps(P))
            q["chainlink"]["USDT"][cle] = valeur
            with self.assertRaises(socle.Refus) as r:
                socle.oracles(q)
            self.assertEqual((r.exception.code, "actif USDT" in str(r.exception)), ("CA/chainlink", True))

    def test_ecrire(self):
        """Étiquette mot pour mot en première ligne (E-CA-04) ; .partiel puis renommage : renommage en échec, la cible
        n'existe pas (E-CA-05). Mutations : étiquette changée ; écriture directe sans .partiel."""
        d = tempfile.mkdtemp(prefix="ca_ecr_")
        self.addCleanup(shutil.rmtree, d, True)
        chemin = socle.ecrire(d, "s.txt", ["a", "b"])
        with open(chemin, encoding="utf-8") as f:
            self.assertEqual(f.read().split(socle.NL), [
                "préparation de S2-bis ; calibration d'ETH, d'USDC et d'USDT sur historiques publics ; ne lit aucune "
                "donnée de S2 ni de S2-bis", "a", "b", ""])
        self.assertEqual(os.listdir(d), ["s.txt"])
        remplacer, socle.os.replace = socle.os.replace, None
        try:
            with self.assertRaises(TypeError):
                socle.ecrire(d, "t.txt", ["a"])
        finally:
            socle.os.replace = remplacer
        self.assertEqual(sorted(os.listdir(d)), ["s.txt", "t.txt.partiel"])


if __name__ == "__main__":
    unittest.main()
