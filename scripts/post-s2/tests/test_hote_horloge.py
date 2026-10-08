"""SHOGEN-HOST-DEGRADED-2 et SHOGEN-HORLOGE-ETENDUE-1 : rattachement des diagnostics aux démarrages, fenêtres retirées
et étendue des offsets attendues à la main ; règle recalculée comparée à r1.analysis_pools puis r1.compute_r1 sur les
fenêtres restantes (attendu métamorphique). Chaque test nomme la mutation qui le rougit."""
import json
import os
import tempfile
import unittest
from decimal import Decimal

import commun
import hote_horloge
from shogen_s2 import records
from tests import fixtures as fx

WS = [fx.VEN + 60 * i for i in range(6)]


def asn(ok, ts):
    return records.asn_attribution_record("h", ["a"], ts, ["r"], {"status": "ok" if ok else "resolve_failed"})


def horloge(ts, med):
    return records.clock_check_record(ts, "startup", {}, {}, med, None if med is not None else "non évaluable")


def controle(dossier):
    """Démarrage 1 (sonde ASN avec un échec) : w0, w1, w2 ; démarrage 2 (sonde propre) : w3, w4, w5 et w1 re-collectée ;
    une sonde ASN finale en échec, rattachée à aucun démarrage ; e n'a de lecture ok qu'en w0 et w2."""
    lignes = [asn(True, WS[0] - 9), asn(False, WS[0] - 8), fx.params(), horloge(WS[0] + 1, 1.5),
              *(fx.marqueur(w) for w in WS[:3]), asn(True, WS[3] - 9), fx.params(), horloge(WS[3] + 1, None),
              *(fx.marqueur(w) for w in WS[3:]), fx.marqueur(WS[1]), asn(False, WS[5] + 70)]
    lect = [fx.lecture(w, f, "panne_transport" if (f in "ab" and k % 2) or (f == "e" and k not in (0, 2)) else "ok")
            for k, w in enumerate(WS) for f in fx.POOL]
    return fx.ecrire(dossier, lignes, lect)


class TestHoteHorloge(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="pp_hote_")

    def test_demarrages_et_fenetres_retirees(self):
        """Deux démarrages ; la sonde en échec est rattachée au premier (elle précède son run_params) ; w1, re-collectée
        au second (dernier marqueur), reste : retirées w0 et w2. Rougit si : sonde rattachée au démarrage précédent ;
        premier marqueur au lieu du dernier ; clock_check qui ouvre un démarrage après un run_params."""
        controle(self.d)
        groupes, attente, _hors = hote_horloge.demarrages(os.path.join(self.d, "control.jsonl"))
        self.assertEqual([(len(g["asn"]), len(g["clock"]), g["ws"]) for g in groupes],
                         [(2, 1, WS[:3]), (1, 1, WS[3:] + [WS[1]])])
        self.assertEqual(len(attente), 1)
        self.assertEqual(hote_horloge.retirees(groupes), {WS[0], WS[2]})

    def test_clock_check_apres_marqueurs_compte(self):
        """Constat de l'exécution (journal G1 §3) : run_params, marqueur w0, puis clock_check et marqueur w1 : le
        clock_check ouvre un démarrage (lecture du §2) ; compté, avec ses fenêtres retenues (w1). Rougit si le compte
        omet ces démarrages ou leurs fenêtres."""
        lignes = [asn(False, WS[0] - 9), fx.params(), fx.marqueur(WS[0]), horloge(WS[1] - 30, 1.0), fx.marqueur(WS[1])]
        fx.ecrire(self.d, lignes, [fx.lecture(w, f) for w in WS[:2] for f in fx.POOL])
        groupes = hote_horloge.demarrages(os.path.join(self.d, "control.jsonl"))[0]
        self.assertEqual(hote_horloge.entrelaces(groupes, {WS[0], WS[1]}), (1, 1))

    def test_sensibilite_egale_au_recalcul_sur_les_fenetres_restantes(self):
        """w0 et w2 retirées : n = 4, et e, sans lecture ok restante, sort du pool par D1. Rougit si les fenêtres
        retirées restent au calcul ou si D1 n'est pas réappliqué sur les fenêtres restantes."""
        controle(self.d)
        d = commun.charger(self.d, {"t0": WS[0], "n_fixe": 6}, [(0, 0)])
        s = hote_horloge.hote_degrade(d)
        m = [x for x in d["markers"] if x["window_start"] not in (WS[0], WS[2])]
        pools = commun.r1.analysis_pools(m, d["readings"], list(fx.POOL))[0]
        self.assertEqual(s["r1"], commun.calculer(d, m, pools))
        self.assertEqual((s["r1"]["strates"]["calme"]["n"], pools["calme"]), (4, ["a", "b", "c", "d"]))

    def test_horloge_etendue(self):
        """Offsets médians retenus 1.5 et None (deux démarrages), plus 3 relevés ajoutés : −0.25, 3.0 dans le segment,
        100 hors du segment (exclu) : n = 4, non évaluable 1, min −0.25, médiane 1.5, max 3.0, étendue 3.25 (à la
        main). Rougit si : relevé hors segment compté ; médiane nulle comptée ; étendue = max seul."""
        controle(self.d)
        with open(os.path.join(self.d, "control.jsonl"), "a", encoding="utf-8") as f:
            for ts, med in ((WS[2] + 5, -0.25), (WS[4] + 5, 3.0), (WS[5] + 600, 100.0)):
                f.write(json.dumps(horloge(ts, med)) + "\n")
        h = hote_horloge.horloge(commun.charger(self.d, {"t0": WS[0], "n_fixe": 6}, [(0, 0)]))
        self.assertEqual((h["n"], h["non_evaluables"], h["min"], h["mediane"], h["max"], h["etendue"]),
                         (4, 1, Decimal("-0.25"), Decimal("1.5"), Decimal("3.0"), Decimal("3.25")))

    def test_horloge_offsets_non_dyadiques_compte_pair(self):
        """Correction G2 C-3 : offsets 0.1, 0.2, 0.7, 1.3 (non dyadiques, compte pair) : minimum 0.1, médiane 0.45
        (moyenne des deux centraux), maximum 1.3, étendue 1.2, Decimal exacts du texte JSON (à la main). Rougit si :
        Decimal du flottant binaire au lieu de son texte court (0.1000000000000000055…) ; médiane haute (0.7)."""
        fx.ecrire(self.d, [fx.params(), *(horloge(w + 5, m) for w, m in zip(WS, (0.1, 0.2, 0.7, 1.3))),
                           *map(fx.marqueur, WS)], [fx.lecture(w, f) for w in WS for f in fx.POOL])
        h = hote_horloge.horloge(commun.charger(self.d, {"t0": WS[0], "n_fixe": 6}, [(0, 0)]))
        self.assertEqual((h["n"], h["non_evaluables"], h["min"], h["mediane"], h["max"], h["etendue"]),
                         (4, 0, Decimal("0.1"), Decimal("0.45"), Decimal("1.3"), Decimal("1.2")))
        self.assertEqual(h["lignes"][-1], "minimum = 0.1 s ; médiane = 0.45 s ; maximum = 1.3 s ; étendue = 1.2 s")


if __name__ == "__main__":
    unittest.main()
