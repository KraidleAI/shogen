"""Lot « filtre d'exclusion » (ADR-0025 déc. 2) : le lecteur retire des plages FERMÉES de
`window_start` de n, K, P̂_more, jamais par excision du journal ; chaque test nomme la
MUTATION qui le rougit (D-4 (b)) ; les valeurs d'ADR-0025 ne vivent qu'ici. Fixture :
w0..w5 = ven. 23:57Z → sam. 00:02Z (w0-w2 calme, w3-w5 stress), REPRISE w1..w3 (doublons
w1 HORS plage, w2 et w3 DANS) ; plage [w2 ; w4] sur des débuts de fenêtre des deux strates,
w4 = fenêtre de la plage à écriture unique (l'analogue des 410 d'ADR-0025)."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from datetime import datetime, timezone

from shogen_s2 import collector, lm, r1, r2, records, report, window
from tests.test_collector import (BY_ID, DELTA, SKELETON, TAU, W, FakeClock, _taumap,
                                  frozen_read_fn, sbc_huge)

WS = [int(datetime(2026, 8, 7, 23, 57, tzinfo=timezone.utc).timestamp()) + i * W
      for i in range(6)]
PLAGE = (WS[2], WS[4])
# (iv) sha256 du rendu SANS option sur l'arbre de BASE (capture_golden_base.py, livrables G1).
SHA_BASE_SANS_OPTION = "a4ffc3e58ec5bc16159b4d90eabfc035094256c3ae1efcbdde598dde75f649a5"
SHA_CONTROL_SCELLE = "351f51b2e4b7421b4ee286c27465cde239124d6edd70c0e550741d22f83366ff"
HARNESS = os.path.dirname(os.path.dirname(os.path.abspath(report.__file__)))


def build_fixture(d: str) -> tuple:
    """Campagne w0..w5 puis reprise w1..w3, écrites dans `d` ; rend (control, journal)."""
    paths = [os.path.join(d, n) for n in ("control.jsonl", "journal.jsonl", "raw.jsonl")]
    for wins in (WS, WS[1:4]):
        clock = [float(wins[0])]
        for b in wins:
            clock += [float(b) + 1.0, float(b) + W - DELTA]
        collector.collect([BY_ID[f] for f in SKELETON], *paths, n_windows=len(wins),
                          sigma_by_class=sbc_huge(), tau_classe=_taumap(TAU),
                          strate_spec=window.WEEKEND_STRATE_SPEC, now_fn=FakeClock(clock),
                          sleep_fn=lambda s: None, read_fn=frozen_read_fn)
    return paths[0], paths[1]


def cli(d: str, *ranges, seed: str = "0") -> bytes:
    """Chemin SERVI (RUNBOOK §9 e) dans un processus neuf, PYTHONHASHSEED imposé."""
    args = [sys.executable, "-m", "shogen_s2.report", d]
    for a, b in ranges:
        args += ["--exclude-window-start-range", str(a), str(b)]
    return subprocess.run(args, cwd=HARNESS, env=dict(os.environ, PYTHONHASHSEED=seed),
                          capture_output=True, check=True).stdout


class TestExclusionFixture(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2excl_")
        self.control, self.journal = build_fixture(self.d)

    def _n(self, ranges):
        """n par strate, le MÊME aux quatre points d'entrée recalculables (C-2, CA-9)."""
        c, j = self.control, self.journal
        out = r1.recompute_from_journal(c, j, exclude_ranges=ranges)
        n = {st: blk["n"] for st, blk in out["strates"].items()}
        out_lm = lm.recompute_lm_from_journal(c, j, exclude_ranges=ranges)
        self.assertEqual({st: blk["n"] for st, blk in out_lm["strates"].items()}, n)
        out_r2 = r2.recompute_r2_from_journal(c, j, exclude_ranges=ranges)
        self.assertEqual(out_r2["content"]["n_windows"], sum(n.values()))
        txt = report.render_report(c, j, exclude_ranges=ranges)
        for st, k in n.items():
            self.assertIn(f"strate « {st} » : n = {k} fenêtres complétées", txt)  # bloc 3
            self.assertIn(f"strate « {st} » : n = {k} ; Σ", txt)                   # bloc 4
        self.assertIn(f"(b) AXE CONTENU (§4.2) — {sum(n.values())} fenêtres", txt)  # bloc 5
        b2 = txt.split("[BLOC 2]")[1].split("[BLOC 3]")[0]                         # bloc 2
        ws2 = {int(t[0]) for t in map(str.split, b2.splitlines()) if t and t[0].isdigit()}
        self.assertEqual(len(ws2), sum(n.values()))
        return n

    def test_i_n_exact_bornes_fermees_doublons(self):
        """(i) Rougit si : borne exclusive ([w2;w4) garde w4 stress, (w2;w4] garde w2 calme) ;
        plage ignorée dans une strate ; dédup cassé (w1 doublé hors plage) ; plage ignorée
        par un des quatre points d'entrée ; plage inversée acceptée (exclusion vide muette)."""
        self.assertEqual(self._n(()), {"calme": 3, "stress": 3})
        self.assertEqual(self._n([PLAGE]), {"calme": 2, "stress": 1})
        with self.assertRaises(ValueError):
            self._n([PLAGE[::-1]])

    def test_garde_53_voit_les_marqueurs_exclus(self):
        """w3 (samedi, DANS la plage) ré-étiqueté « calme » lève toujours, aux quatre points
        d'entrée. Rougit si : filtre appliqué AVANT verify_markers_against_spec."""
        with open(self.control, encoding="utf-8") as fh:
            objs = [json.loads(ln) for ln in fh if ln.strip()]
        for o in objs:
            if o.get("record") == "window_close" and o["window_start"] == WS[3]:
                o["strate"] = "calme"
        with open(self.control, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(o, ensure_ascii=False) + "\n" for o in objs)
        for fn in (r1.recompute_from_journal, lm.recompute_lm_from_journal,
                   r2.recompute_r2_from_journal, report.render_report):
            with self.assertRaises(ValueError):
                fn(self.control, self.journal, exclude_ranges=[PLAGE])

    def test_iii_deterministe_et_bloc1_par_la_cli(self):
        """(iii) Deux processus (PYTHONHASHSEED 1 et 2, plages en ordre inverse) ⇒ mêmes
        octets, = l'API ; bloc 1 : chaque plage en epoch ET ISO-8601 UTC, avec le motif.
        Rougit si : tri des plages retiré ; paramètres absents du bloc 1 ; option non transmise."""
        deux = [(WS[4], WS[4]), (WS[2], WS[3])]
        self.assertEqual(self._n(deux), {"calme": 2, "stress": 1})  # union des deux plages
        out = cli(self.d, *deux, seed="1")
        self.assertEqual(out, cli(self.d, *deux[::-1], seed="2"))
        api = report.render_report(self.control, self.journal, exclude_ranges=deux)
        self.assertEqual(out, (api + "\n").encode("utf-8"))
        bloc1 = api.split("[BLOC 2]")[0]
        for a, b in sorted(deux):
            iso = [datetime.fromtimestamp(t, timezone.utc).isoformat() for t in (a, b)]
            self.assertIn(f"= [{a} ; {b}] = [{iso[0]} ; {iso[1]}] fermée", bloc1)
        self.assertEqual(bloc1.count("harnais dégradé, ADR-0025"), 2)

    def test_iv_sans_option_octets_d_avant_le_lot(self):
        """(iv) Sans option : les octets d'AVANT le lot (sha de l'arbre de base), et la CLI
        RUNBOOK §9 e les émet telle quelle. Rougit si : une ligne est ajoutée sans filtre
        (ex. « exclusion : aucune ») ; la CLI sans option change de sortie."""
        txt = report.render_report(self.control, self.journal)
        self.assertEqual(hashlib.sha256(txt.encode("utf-8")).hexdigest(), SHA_BASE_SANS_OPTION)
        self.assertEqual(cli(self.d), (txt + "\n").encode("utf-8"))


class TestExclusionJournalReel(unittest.TestCase):
    def test_ii_plage_adr0025_retire_2618_fenetres(self):
        """(ii) control.jsonl RÉEL scellé (copie ; n = marqueurs) via SHOGEN_S2_CAMPAGNE_CONTROL,
        sinon SkipTest explicite. ADR-0025 déc. 1, borne haute amendée (décision 272) [2026-09-24T18:18Z
        ; 2026-09-26T15:08Z] : 38 600 → 35 982 (−2 618 = 1 709 + 909). Rougit si : borne exclusive
        (2 617) ; strate ignorée."""
        path = os.environ.get("SHOGEN_S2_CAMPAGNE_CONTROL")
        if not path:
            raise unittest.SkipTest("SHOGEN_S2_CAMPAGNE_CONTROL absente : copie du control.jsonl"
                                    " scellé non fournie, test (ii) NON exécuté")
        with open(path, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), SHA_CONTROL_SCELLE)
        params_list, _clock, markers = records.parse_control(path)
        params = records.effective_run_params(params_list)
        self.assertEqual(window.verify_markers_against_spec(markers, params["strate_calendar"]), [])
        a, b = (int(datetime(2026, 9, d, h, m, tzinfo=timezone.utc).timestamp())
                for d, h, m in ((24, 18, 18), (26, 15, 8)))
        avant = Counter(r1.build_window_strate(markers).values())
        apres = Counter(r1.build_window_strate(
            records.exclude_window_start_ranges(markers, [(a, b)])).values())
        self.assertEqual(avant, Counter(calme=26294, stress=12306))       # 38 600
        self.assertEqual(apres, Counter(calme=24585, stress=11397))       # 35 982
        self.assertEqual(avant - apres, Counter(calme=1709, stress=909))  # 2 618


if __name__ == "__main__":
    unittest.main()
