"""G2 lot A (ADR-0025, reviseur claude-opus-5-5, 2026-09-29) : tests ADVERSARIAUX ecrits dans la
copie de travail F:/tmp/shogen-g2-lotA/corr, jamais dans le depot. Ils FIGENT la semantique
constatee (window_start dans [from, to], bornes incluses) sur les cas que le G1 n'a pas testes ;
ils passent sur le code du lot (742f1fc). Fixture : celle du lot (build_fixture, w0..w5,
w0-w2 calme, w3-w5 stress, reprise w1..w3)."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
import unittest

from shogen_s2 import lm, r1, r2, records, report
from tests import test_exclusion as te   # module, pas la classe : evite une double decouverte
from tests.test_collector import W

WS, PLAGE = te.WS, te.PLAGE
SANS = {"calme": 3, "stress": 3}


def _cli(d, *args):
    return subprocess.run([sys.executable, "-B", "-m", "shogen_s2.report", d, *args],
                          cwd=te.HARNESS, capture_output=True, text=True, encoding="utf-8",
                          errors="replace",
                          # l'enfant écrit en UTF-8 quel que soit l'encodage de la console
                          # (cp1252 sous Windows sans -X utf8 : « inversée » illisible sinon)
                          env=dict(os.environ, PYTHONIOENCODING="utf-8"))


class TestG2Adversarial(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2g2adv_")
        self.control, self.journal = te.build_fixture(self.d)

    def _n(self, ranges):
        return te.TestExclusionFixture._n(self, ranges)   # memes 4 points d'entree + rendu

    def test_bornes_egales_une_seule_fenetre(self):
        """[ws ; ws] retire exactement la fenetre ws (doublee ou non), aux quatre points."""
        for i, ws in enumerate(WS):
            st = "calme" if i < 3 else "stress"
            attendu = dict(SANS, **{st: SANS[st] - 1})
            self.assertEqual(self._n([(ws, ws)]), attendu, (i, ws))

    def test_plage_hors_campagne_sans_effet_ligne_bloc1_seule(self):
        """Plages avant w0 et apres w5 : n inchange ; le rendu ne differe du rendu sans option
        QUE par les lignes du bloc 1 (B-SEG-2 : comptes à 0 visibles, tests/test_bloc1.py)."""
        rs = [(WS[0] - 10 * W, WS[0] - W), (WS[5] + W, WS[5] + 9 * W)]
        self.assertEqual(self._n(rs), SANS)
        avec = report.render_report(self.control, self.journal, exclude_ranges=rs)
        sans = report.render_report(self.control, self.journal)
        lignes = [ln for ln in avec.split("\n") if not ln.startswith("  exclusion_")]   # 4 clés (B-SEG-2)
        self.assertEqual("\n".join(lignes), sans)
        self.assertEqual(avec.count("exclusion_window_start"), 2)

    def test_plage_inversee_leve_a_chaque_point_d_entree_et_cli_rc1(self):
        for fn in (r1.recompute_from_journal, lm.recompute_lm_from_journal,
                   r2.recompute_r2_from_journal, report.render_report):
            with self.assertRaises(ValueError, msg=fn.__qualname__):
                fn(self.control, self.journal, exclude_ranges=[PLAGE[::-1]])
        p = _cli(self.d, "--exclude-window-start-range", str(PLAGE[1]), str(PLAGE[0]))
        self.assertEqual(p.returncode, 1)
        self.assertIn("inversée", p.stderr)
        self.assertEqual(p.stdout, "")

    def test_cli_non_entier_et_negatif_rc2(self):
        for a in ("1.5", "abc"):
            self.assertEqual(_cli(self.d, "--exclude-window-start-range", a, "2").returncode, 2)
        p = _cli(self.d, "--exclude-window-start-range", "-5", "10")   # G1 §10-4 ; refusé (B-SEG-2, Q-G2-5)
        self.assertEqual((p.returncode, p.stdout), (2, ""))
        self.assertIn("SHOGEN-NEG-EPOCH-1", p.stderr)

    def test_fenetre_a_cheval_bornes_hors_grille(self):
        """[w2+30 ; w4+30] : w2 (a cheval sur la borne basse) RETENUE, w3 et w4 exclues."""
        self.assertEqual(self._n([(WS[2] + 30, WS[4] + 30)]), {"calme": 3, "stress": 1})

    def test_plages_chevauchantes_et_emboitees(self):
        self.assertEqual(self._n([(WS[1], WS[3]), (WS[2], WS[4])]), {"calme": 1, "stress": 1})
        self.assertEqual(self._n([(WS[0], WS[5]), (WS[2], WS[3])]), {})
        txt = report.render_report(self.control, self.journal,
                                   exclude_ranges=[(WS[0], WS[5]), (WS[2], WS[3])])
        self.assertIn("aucune fenêtre complétée (n = 0)", txt)

    def test_plage_vidant_une_strate(self):
        self.assertEqual(self._n([(WS[3], WS[5])]), {"calme": 3})
        txt = report.render_report(self.control, self.journal, exclude_ranges=[(WS[3], WS[5])])
        self.assertNotIn("strate « stress »", txt)

    def test_doublons_tous_les_marqueurs_d_une_fenetre_exclue_retires(self):
        """Dedup last-wins : les DEUX marqueurs de w2 et w3 (doublees, dans la plage) sont
        retires, w1 (doublee, hors plage) garde ses deux marqueurs ; entree non mutee."""
        _p, _c, markers = records.parse_control(self.control)
        compte = lambda ms: sorted(int(m["window_start"]) for m in ms)
        avant = compte(markers)
        self.assertEqual(avant, sorted(WS + WS[1:4]))
        garde = records.exclude_window_start_ranges(markers, [PLAGE])
        self.assertEqual(compte(garde), sorted([WS[0], WS[1], WS[1], WS[5]]))
        self.assertEqual(compte(markers), avant)
        self.assertEqual(sorted(r1.build_window_strate(garde)), [WS[0], WS[1], WS[5]])

    def test_journal_intact_apres_rendu_filtre(self):
        def h(p):
            with open(p, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        avant = (h(self.control), h(self.journal))
        report.render_report(self.control, self.journal, exclude_ranges=[PLAGE])
        _cli(self.d, "--exclude-window-start-range", str(PLAGE[0]), str(PLAGE[1]))
        self.assertEqual((h(self.control), h(self.journal)), avant)

    def test_epochs_adr0025_ratifies_en_iso(self):
        """Valeurs de la commande J28 (ADR-0025 amendee, decision 272) : 1790273880 ; 1790435280."""
        self.assertEqual(report._iso_utc(1790273880), "2026-09-24T18:18:00+00:00")
        self.assertEqual(report._iso_utc(1790435280), "2026-09-26T15:08:00+00:00")
        self.assertEqual(report._iso_utc(1790435220), "2026-09-26T15:07:00+00:00")


if __name__ == "__main__":
    unittest.main()
