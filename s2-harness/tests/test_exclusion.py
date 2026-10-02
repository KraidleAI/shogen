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
from itertools import count

from shogen_s2 import collector, lm, r1, r2, records, report, window
from tests.test_collector import (BY_ID, DELTA, SKELETON, TAU, W, FakeClock, _taumap,
                                  frozen_read_fn, sbc_huge)

WS = [int(datetime(2026, 8, 7, 23, 57, tzinfo=timezone.utc).timestamp()) + i * W
      for i in range(6)]
PLAGE = (WS[2], WS[4])
# (iv) sha256 du rendu SANS option, re-capturé à chaque sous-lot de B-SEG-2 qui ajoute une ligne au bloc 1
# (P2P ligne à ligne : insertions seules, docs/G1-lot-B-SEG-2-bloc1.md) ; lot A : a4ffc3e5…f649a5 ; puis au
# sous-lot B-b (blocs 3 et 6 ; avant b054a0f4…69ac01e ; P2P texte : docs/G1-lot-B-sensibilite.md) ; puis au
# sous-lot POOLEE-b (bloc 3 : famille et strate poolée ; avant 9518d21b…4b62a92 ; P2P texte :
# docs/G1-lot-POOLEE-strate-poolee.md) ; puis au lot B-DEP-2 (bloc 3 : z_bloc par strate et
# A(window-dependence) ; avant a3b5f0f8…906f954 ; P2P texte : docs/G1-lot-B-DEP-2-bloc3.md) ; puis au
# sous-lot CRITERE-a2 (bloc 3 : famille, section règle ; avant aec8409c…c20b6bd ; P2P texte :
# docs/G1-lot-CRITERE-regle.md) ; puis au sous-lot CRITERE-b2 (bloc 6 : ligne d'entrées du drapeau 2 ;
# avant 8e01c22f…27cf13b ; même journal) ; puis au sous-lot D5-AMEND-b (bloc 1 : fenêtres sautées ; bloc 3 :
# traitements de l'annexe D.5 ; avant ac530cec…bcf8 ; P2P texte : docs/G1-lot-D5-AMEND-descriptifs.md).
SHA_BASE_SANS_OPTION = "a7f5cbfda5295a25e5c4dfa8b1700843af96fc92e3b77dbfc2be632fa72bb544"
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


def poser(d: str, instants) -> None:
    """Sur chaque instant t : démarrage sans fenêtre du collecteur réel (run_params, clock_check à
    harness_ts = t) et sonde ASN datée t (r2.collect_asn), un AS distinct par appel et par hôte."""
    c, j, raw = (os.path.join(d, n) for n in ("control.jsonl", "journal.jsonl", "raw.jsonl"))
    specs, asn = [BY_ID[f] for f in SKELETON], count(64512)

    def resolve(host, resolvers):
        a = next(asn)
        return {"status": "ok", "asn_ripestat": a, "asn_cymru": a}
    for t in map(float, instants):
        collector.collect(specs, c, j, raw, n_windows=0, sigma_by_class=sbc_huge(), tau_classe=_taumap(TAU),
                          strate_spec=window.WEEKEND_STRATE_SPEC, now_fn=FakeClock([t]),
                          sleep_fn=lambda s: None, read_fn=frozen_read_fn)
        r2.collect_asn(specs, c, resolve_fn=resolve, now_fn=lambda t=t: t)


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

    def test_v_window_start_bornes_a_une_seconde(self):
        """(v) G2 B-SEG-1 : [w3 + 1 ; w4] garde w3 (= A − 1) ; [w2 ; w3 − 1] garde w3 (= B + 1), aux quatre
        points. Rougit si : A − 1 ou B + 1 inclus sur la branche window_start (prédicat fermé propre)."""
        self.assertEqual(self._n([(WS[3] + 1, WS[4])]), {"calme": 3, "stress": 2})
        self.assertEqual(self._n([(WS[2], WS[3] - 1)]), {"calme": 2, "stress": 3})

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
        """(iv) Sans option : les octets épinglés (lot A ; re-capture justifiée de B-SEG-2, HS2-05), et la
        CLI RUNBOOK §9 e les émet telle quelle. Rougit si : une ligne du rendu sans option change sans
        re-capture justifiée (ex. « exclusion : aucune ») ; la CLI sans option change de sortie."""
        txt = report.render_report(self.control, self.journal)
        self.assertEqual(hashlib.sha256(txt.encode("utf-8")).hexdigest(), SHA_BASE_SANS_OPTION)
        self.assertEqual(cli(self.d), (txt + "\n").encode("utf-8"))


A, B = PLAGE                                   # D5 : clock_check et asn posés sur A − 1, A, B, B + 59, B + 60


class TestExclusionTousTypes(unittest.TestCase):
    """ADR-0028 D5 (SHOGEN-EXCL-TOUS-TYPES-1) : la plage [A ; B] retire aussi clock_check (harness_ts) et
    asn_attribution (ts) de [A ; B + w) ; window_start reste fermé [A ; B] (tests (i) et à cheval du G2)."""

    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2d5_")
        self.control, self.journal = build_fixture(self.d)
        poser(self.d, (A - 1, A, B, B + 59, B + 60))

    def test_d5_bornes_par_type_aux_points_d_entree_et_cli(self):
        """Gardés : A − 1, B + 60 (et les démarrages w0, w1) ; retirés : A, B, B + 59. Rougit si : borne
        ±1 ; ts ou harness_ts fermé sans + w ; asn ou clock_check non filtré (outil, r2, rendu) ;
        run_params filtré ; type sans règle accepté."""
        c, j = self.control, self.journal
        self.assertEqual(TestExclusionFixture._n(self, [PLAGE]), {"calme": 2, "stress": 1})
        txt = report.render_report(c, j, exclude_ranges=[PLAGE])
        bloc1 = txt.split("[BLOC 2]")[0]
        horloges = records.parse_control(c)[1]
        self.assertEqual(len({h["median_offset"] for h in horloges}), 7)      # lignes discernables
        for h in horloges:
            self.assertEqual(f"médiane_offset(s)={h['median_offset']} sources" in bloc1,
                             h["harness_ts"] in (WS[0], WS[1], A - 1, B + 60), h["harness_ts"])
        self.assertIn(f"{'run_params_demarrages':24} = 7 ", bloc1)            # run_params conservés
        hotes = sorted(set(r2.build_flux_hosts([BY_ID[f] for f in SKELETON]).values()))
        part = r2.recompute_r2_from_journal(c, j, exclude_ranges=[PLAGE])["partition"]
        self.assertEqual([(v["host"], v["avant"][2], v["apres"][2]) for v in part["asn_divergences"]],
                         [(h, A - 1, B + 60) for h in hotes])
        self.assertEqual(txt.count("DIVERGENCE ASN"), len(hotes))
        self.assertEqual(cli(self.d, PLAGE), (txt + "\n").encode("utf-8"))
        with self.assertRaises(ValueError):                 # type sans règle d'horodatage : fail-closed
            records.exclude_window_start_ranges([{"record": "autre", "window_start": A}], [PLAGE])

    def test_d5_deux_plages_sur_ts_et_harness_ts(self):
        """G2 B-SEG-1 : [w0 ; w0] et [B ; B] retirent horloges et sondes de [w0 ; w0 + w) et de
        [B ; B + w) seulement. Rougit si : any remplacé par all (plusieurs plages) sur ts/harness_ts."""
        p, clocks, markers = records.parse_control(self.control)
        _m, c, s, _ = records.filtre_lecture(records.effective_run_params(p), markers, clocks,
                                             records.parse_asn(self.control), [(WS[0], WS[0]), (B, B)])
        self.assertEqual(sorted({x["harness_ts"] for x in c}), [WS[1], A - 1, A, B + 60])
        self.assertEqual(sorted({x["ts"] for x in s}), [A - 1, A, B + 60])

    def test_type_vide_rendu_sans_asn_ni_horloge(self):
        """C-15 : [WS[0] ; WS[5] − 1] retire tout clock_check et tout asn (t < WS[5] + 59) mais garde w5
        (fermée sur window_start) : le rendu sort, axe ASN NON MESURÉ, aucune ligne controle_horloge.
        Rougit si : asn ou clock_check non filtré ; window_start traité en [A ; B + w) (w5 retirée)."""
        rg = [(WS[0], WS[5] - 1)]
        txt = report.render_report(self.control, self.journal, exclude_ranges=rg)
        self.assertEqual((txt.count("controle_horloge"), txt.count("axe ASN NON MESURÉ")), (0, 2))
        self.assertEqual(txt.count("strate « stress » : n = 1 fenêtres complétées"), 1)
        self.assertEqual(cli(self.d, *rg), (txt + "\n").encode("utf-8"))


CLES = ("record", "window_start", "ts", "harness_ts")   # seules clés lues et affichées (ADR-0028 D.4 a pt 2)


def _proj(objs) -> list:
    return [{k: o[k] for k in CLES if k in o} for o in objs]


def comptes_outil(path: str, a: int, b: int, w: int) -> dict:
    """Retirés par l'outil (filtre_lecture) des listes de parse_control et parse_asn, projetées sur CLES."""
    _p, clocks, markers = records.parse_control(path)
    m, c, s = _proj(markers), _proj(clocks), _proj(records.parse_asn(path))
    m2, c2, s2 = records.filtre_lecture({"w": w}, m, c, s, ranges=[(a, b)])[:3]
    fen = lambda ms: len({x["window_start"] for x in ms})
    return {"window_close": fen(m) - fen(m2), "asn_attribution": len(s) - len(s2),
            "clock_check": len(c) - len(c2)}


def recompte_independant(path: str, a: int, b: int, w: int) -> dict:
    """Recompte en bibliothèque standard, sans records : chaque ligne projetée sur CLES dès son décodage."""
    with open(path, encoding="utf-8") as f:
        objs = _proj(json.loads(ln) for ln in f if ln.strip())
    champ = {"asn_attribution": "ts", "clock_check": "harness_ts"}
    out = Counter(o["record"] for o in objs
                  if o.get("record") in champ and a <= o[champ[o["record"]]] < b + w)
    out["window_close"] = len({o["window_start"] for o in objs
                               if o.get("record") == "window_close" and a <= o["window_start"] <= b})
    return dict(out)


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

    def test_ii_plage_adr0025_comptes_par_type(self):
        """(ii bis) Comptes par type de la plage ADR-0025 sur le control.jsonl RÉEL scellé (copie, via
        SHOGEN_S2_CAMPAGNE_CONTROL, sinon SkipTest ; ADR-0028 annexe D.4 a pt 2). Attendus :
        docs/adr-0028/ADR-0028-decisions-sortie-S2.md l.56-57 (D5 : asn_attribution 5 313, clock_check
        483 sur [1790273880 ; 1790435340)) ; window_close 2 618 fenêtres distinctes sur [A ; B] (ADR-0025
        l.3 et l.44 ; test (ii)). Lignes brutes pour asn et clock_check ; repère de rejeu : 5 313 = 11 × 483.
        Outil ET recompte indépendant ; aucune autre clé que record, window_start, ts, harness_ts n'est lue
        ni affichée ; w = 60 s (ADR-0028 l.35), jamais lu de run_params. Divergence au rejeu : escalade,
        jamais le test ajusté à l'outil."""
        path = os.environ.get("SHOGEN_S2_CAMPAGNE_CONTROL")
        if not path:
            raise unittest.SkipTest("SHOGEN_S2_CAMPAGNE_CONTROL absente : copie du control.jsonl scellé non"
                                    " fournie, test de comptes par type NON exécuté")
        with open(path, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), SHA_CONTROL_SCELLE)
        a, b = (int(datetime(2026, 9, d, h, m, tzinfo=timezone.utc).timestamp())
                for d, h, m in ((24, 18, 18), (26, 15, 8)))
        self.assertEqual((a, b, b + 60), (1790273880, 1790435280, 1790435340))   # D5 l.57
        attendu = {"window_close": 2618, "asn_attribution": 5313, "clock_check": 483}
        self.assertEqual(recompte_independant(path, a, b, 60), attendu)
        self.assertEqual(comptes_outil(path, a, b, 60), attendu)


if __name__ == "__main__":
    unittest.main()
