"""Lot B-SEG-1b (ADR-0028 D4, D2 pt 6 ; HS2-08) : segment [t0 ; t_fin), MÊME borne pour window_start, ts
et harness_ts, run_params conservés ; n fixe : t_fin = n-ième window_start distinct ≥ t0, + w, lu avant
segment et exclusion. Module neuf (C-11). Fixture de l'exclusion + poser sur t0 − 1, t0, t_fin − 1, t_fin."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from itertools import count

from shogen_s2 import collector, lm, r1, r2, records, report, window
from tests.test_collector import BY_ID, SKELETON, TAU, FakeClock, _taumap, frozen_read_fn, sbc_huge
from tests.test_exclusion import HARNESS, WS, build_fixture, poser

T0, TF = WS[1], WS[4]        # [w1 ; w4) : w0 avant t0 ; w4 (= t_fin), w5 hors ; w3 (= t_fin − w) dedans
SEG = {"t0": T0, "t_fin": TF}
HOTES = sorted(set(r2.build_flux_hosts([BY_ID[f] for f in SKELETON]).values()))
POINTS = (r1.recompute_from_journal, lm.recompute_lm_from_journal, r2.recompute_r2_from_journal,
          report.render_report)


def cli(d, *args):             # chemin SERVI (RUNBOOK §9 e), processus neuf : (code de retour, stdout)
    p = subprocess.run([sys.executable, "-B", "-m", "shogen_s2.report", d, *map(str, args)], cwd=HARNESS,
                       capture_output=True)
    return p.returncode, p.stdout


class TestSegment(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2seg_")
        self.c, self.j = build_fixture(self.d)
        poser(self.d, (T0 - 1, T0, TF - 1, TF))

    def _n(self, **kw):
        """n par strate, le MÊME aux quatre points d'entrée ; rend (n, rendu)."""
        c, j, par = self.c, self.j, lambda out: {st: b["n"] for st, b in out["strates"].items()}
        n = par(r1.recompute_from_journal(c, j, **kw))
        self.assertEqual(par(lm.recompute_lm_from_journal(c, j, **kw)), n)
        self.assertEqual(r2.recompute_r2_from_journal(c, j, **kw)["content"]["n_windows"], sum(n.values()))
        txt = report.render_report(c, j, **kw)
        for st, k in n.items():
            self.assertIn(f"strate « {st} » : n = {k} fenêtres complétées", txt)
        return n, txt

    def test_bornes_tous_types_aux_quatre_points_et_cli(self):
        """clock_check et asn gardés sur t0 et t_fin − 1, retirés sur t0 − 1, t_fin et w0. Rougit si : borne
        ±1 ; fin incluse ; début exclu ; type non segmenté (outil, r2, rendu) ; segment omis à un point
        d'entrée ; run_params filtrés ; ligne de bloc 1 absente ; option CLI non transmise."""
        n, txt = self._n(segment=SEG)
        self.assertEqual(n, {"calme": 2, "stress": 1})
        bloc1 = txt.split("[BLOC 2]")[0]
        horloges = records.parse_control(self.c)[1]
        self.assertEqual(len({h["median_offset"] for h in horloges}), 5)      # 6 démarrages, 5 instants
        for h in horloges:
            self.assertEqual(f"médiane_offset(s)={h['median_offset']} sources" in bloc1,
                             h["harness_ts"] in (T0, TF - 1), h["harness_ts"])
        self.assertIn(f"{'run_params_demarrages':24} = 6 ", bloc1)
        part = r2.recompute_r2_from_journal(self.c, self.j, segment=SEG)["partition"]
        self.assertEqual([(v["host"], v["avant"][2], v["apres"][2]) for v in part["asn_divergences"]],
                         [(h, T0, TF - 1) for h in HOTES])
        self.assertEqual(txt.count("DIVERGENCE ASN"), len(HOTES))
        iso = [report._iso_utc(t) for t in (T0, TF)]
        self.assertIn(f"{'segment':24} = [{T0} ; {TF}) = [{iso[0]} ; {iso[1]}) semi-ouvert", bloc1)
        self.assertEqual(cli(self.d, "--segment-from", T0, "--segment-to", TF), (0, f"{txt}\n".encode()))

    def test_bornes_hors_grille_et_type_vide(self):
        """[w1 + 1 ; w3 + 1) : w1 (= t0 − 1) hors, w3 (= t_fin − 1) dedans ; C-15 : [w5 ; w5 + w) ne garde
        aucun clock_check ni asn (tous avant w5), le rendu sort. Rougit si : borne ±1 sur window_start ;
        asn ou clock_check non segmenté."""
        self.assertEqual(self._n(segment={"t0": T0 + 1, "t_fin": WS[3] + 1})[0], {"calme": 1, "stress": 1})
        n, txt = self._n(segment={"t0": WS[5], "t_fin": WS[5] + 60})
        self.assertEqual(n, {"stress": 1})
        self.assertEqual((txt.count("controle_horloge"), txt.count("axe ASN NON MESURÉ")), (0, 2))

    def test_n_fixe_lu_du_journal_avant_exclusion(self):
        """n = 3 : t_fin = 3e window_start distinct ≥ t0 (w3), + w = w4, malgré les doublons w1-w3, w0 avant
        t0 et l'exclusion [w2 ; w2] ; mêmes sorties qu'en t_fin explicite, n au bloc 1, CLI. Rougit si :
        doublons comptés ; fenêtre avant t0 comptée ; t_fin calculé après l'exclusion ; + w omis ; rang
        décalé."""
        kw, seg_n = {"exclude_ranges": [(WS[2], WS[2])]}, {"t0": T0, "n_fixe": 3}
        for f in POINTS[:3]:
            self.assertEqual(f(self.c, self.j, segment=seg_n, **kw), f(self.c, self.j, segment=SEG, **kw))
        txt = report.render_report(self.c, self.j, segment=seg_n, **kw)
        self.assertEqual(txt.count("n fixe = 3 —"), 1)
        self.assertEqual(txt.replace("n fixe = 3 —", "n fixe = - —"),
                         report.render_report(self.c, self.j, segment=SEG, **kw))
        self.assertEqual(cli(self.d, "--segment-from", T0, "--segment-n-fixe", 3,
                             "--exclude-window-start-range", WS[2], WS[2]), (0, f"{txt}\n".encode()))

    def test_moins_de_n_fenetres_leve_jamais_silencieux(self):
        """5 fenêtres distinctes ≥ t0 : n = 5 rend t_fin = w5 + w ; n = 6 : rc 1 à la CLI (ValueError aux
        quatre points : test suivant). Rougit si : t_fin silencieux sous n (dernière fenêtre, rang borné)."""
        self.assertEqual(self._n(segment={"t0": T0, "n_fixe": 5})[0], {"calme": 2, "stress": 3})
        self.assertEqual(cli(self.d, "--segment-from", T0, "--segment-n-fixe", 6), (1, b""))

    def test_segment_incomplet_double_ou_vide_refuse(self):
        """CLI rc 2 : début seul, fin seule, n seul, deux fins ; API : segment vide ou inversé (t0 ≥ t_fin),
        sans fin, à deux fins, n = 6 ou n = 0 ⇒ ValueError aux quatre points. Rougit si : exclusivité des
        fins retirée ; segment partiel accepté ; segment vide accepté ; t_fin silencieux sous n."""
        for args in (("--segment-from", T0), ("--segment-to", TF), ("--segment-n-fixe", 3),
                     ("--segment-from", T0, "--segment-to", TF, "--segment-n-fixe", 3)):
            self.assertEqual(cli(self.d, *args)[0], 2, args)
        for seg in ({"t0": TF, "t_fin": TF}, {"t0": TF, "t_fin": T0}, {"t0": T0}, dict(SEG, n_fixe=3),
                    {"t0": T0, "n_fixe": 6}, {"t0": T0, "n_fixe": 0}):
            for f in POINTS:
                with self.assertRaises(ValueError, msg=(f.__qualname__, seg)):
                    f(self.c, self.j, segment=seg)

    def test_garde_53_sur_tous_les_marqueurs(self):
        """w5 (hors segment) ré-étiquetée « calme » lève aux quatre points. Rougit si : garde §5.3
        appliquée après le segment."""
        with open(self.c, encoding="utf-8") as fh:
            objs = [json.loads(ln) for ln in fh if ln.strip()]
        for o in objs:
            if o.get("record") == "window_close" and o["window_start"] == WS[5]:
                o["strate"] = "calme"
        with open(self.c, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(o, ensure_ascii=False) + "\n" for o in objs)
        for f in POINTS:
            with self.assertRaises(ValueError):
                f(self.c, self.j, segment=SEG)

    def test_run_params_hors_segment_toujours_verifies(self):
        """Démarrage à τ divergent posé hors segment (w5 + 2w) : lève aux quatre points. Rougit si :
        run_params filtrés par le segment avant la concordance (§E)."""
        collector.collect([BY_ID[f] for f in SKELETON], self.c, self.j, os.path.join(self.d, "raw.jsonl"),
                          n_windows=0, sigma_by_class=sbc_huge(), tau_classe=_taumap(TAU * 2),
                          strate_spec=window.WEEKEND_STRATE_SPEC, now_fn=FakeClock([float(WS[5] + 120)]),
                          sleep_fn=lambda s: None, read_fn=frozen_read_fn)
        for f in POINTS:
            with self.assertRaises(ValueError):
                f(self.c, self.j, segment=SEG)


WS120 = [WS[0] - 60 + 120 * i for i in range(6)]   # G2 B-SEG-1 : grille à w = 120 s (23:56Z, multiple de 120)


def fixture_w120(d, instants):
    """Campagne du collecteur réel à w = 120 s, puis démarrages sans fenêtre et sondes ASN aux instants."""
    c, j, raw = (os.path.join(d, n) for n in ("control.jsonl", "journal.jsonl", "raw.jsonl"))
    specs, asn = [BY_ID[f] for f in SKELETON], count(64512)
    kw = dict(w=120, sigma_by_class=sbc_huge(), tau_classe=_taumap(TAU), sleep_fn=lambda s: None,
              strate_spec=window.WEEKEND_STRATE_SPEC, read_fn=frozen_read_fn)
    clock = [float(WS120[0])] + [t for b in WS120 for t in (b + 1.0, b + 115.0)]
    collector.collect(specs, c, j, raw, n_windows=6, now_fn=FakeClock(clock), **kw)
    for t in map(float, instants):
        collector.collect(specs, c, j, raw, n_windows=0, now_fn=FakeClock([t]), **kw)
        a = next(asn)
        r2.collect_asn(specs, c, now_fn=lambda t=t: t,
                       resolve_fn=lambda h, r, a=a: {"status": "ok", "asn_ripestat": a, "asn_cymru": a})
    return c, j


class TestSegmentW120(unittest.TestCase):
    def test_w_lu_de_run_params_exclusion_et_n_fixe(self):
        """G2 B-SEG-1 : w = 120 (run_params). [ws2 ; ws3] retire horloges et sondes jusqu'à B + 119, garde
        B + 120 ; n fixe = 2 depuis ws1 : t_fin = ws2 + 120, garde ws2 + 90. Rougit si : w codé en dur à 60
        (outil ou n fixe)."""
        A, B = WS120[2], WS120[3]
        c, _j = fixture_w120(tempfile.mkdtemp(prefix="s2w120_"), (A - 1, A + 90, B + 60, B + 119, B + 120))
        p, clocks, markers = records.parse_control(c)
        params, asn = records.effective_run_params(p), records.parse_asn(c)
        _m, k, s, _ = records.filtre_lecture(params, markers, clocks, asn, [(A, B)])
        self.assertEqual(sorted({x["harness_ts"] for x in k}), [WS120[0], A - 1, B + 120])
        self.assertEqual(sorted({x["ts"] for x in s}), [A - 1, B + 120])
        _m, k, _s, seg = records.filtre_lecture(params, markers, clocks, asn,
                                                segment={"t0": WS120[1], "n_fixe": 2})
        self.assertEqual((seg, sorted({x["harness_ts"] for x in k})), ((WS120[1], B), [A - 1, A + 90]))

if __name__ == "__main__":
    unittest.main()
