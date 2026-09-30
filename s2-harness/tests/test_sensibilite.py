"""Lot B d'ADR-0028 (ADR-0025 déc. 4 ; D2 pt 7, §1 bis.1 pt 9) : section [SENSIBILITÉ], variante « plage
incluse » (R1 seul, pool D1 de la variante), couverture par week-end. Oracle hors du doré (C-4 du cp-1
de B) : cellules = r1.recompute_from_journal avec et sans plages (même segment), écart recalculé ici en
Decimal, week-ends recomptés en bibliothèque standard depuis control.jsonl (B-a2). Fixture :
collecteur réel à w = 3600 s, statuts scriptés ; blocs ven. 08-07 22:00Z → lun. 08-10 01:00Z, ven. 08-14
23:00Z → sam. 08-15 05:00Z, sam. 08-22 00:00Z → 02:00Z, puis reprise de sam. 08-08 00:00Z et 01:00Z.
Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from decimal import localcontext

from shogen_s2 import collector, r1, report, window
from shogen_s2.model import Reading, Status
from tests.test_collector import BY_ID, DELTA, SKELETON, TAU, FakeClock, _taumap, frozen_reading, sbc_huge
from tests.test_exclusion import HARNESS, PLAGE, build_fixture

H, PLEIN = 3600, 2 * 86400 // 3600       # w de la fixture (run_params) ; fenêtres d'un week-end complet


def t(jour: int, heure: int) -> int:
    return int(datetime(2026, 8, jour, heure, tzinfo=timezone.utc).timestamp())


BLOCS = [range(t(7, 22), t(10, 2), H), range(t(14, 23), t(15, 6), H), range(t(22, 0), t(22, 3), H),
         range(t(8, 0), t(8, 2), H)]                              # le dernier : reprise (doublons)
RA, RB = (t(14, 23), t(15, 4)), (t(22, 0), t(22, 2))
STRESS = sorted({ws for b in BLOCS for ws in b if datetime.fromtimestamp(ws, timezone.utc).weekday() >= 5})
SEG = {"t0": t(7, 22), "n_fixe": 60}       # forme J28 : t_fin = 60e fenêtre distincte + w = t(22, 1)


def panne(f: str, ws: int) -> bool:
    """Stress : coinbase et kraken en panne aux rangs impairs, bitstamp aux multiples de 3 (z publié) ;
    calme : bitstamp n'a de lecture ok qu'à t(14, 23), dans RA (D1 cas b dans la variante exclue seule)."""
    if ws in STRESS:
        return STRESS.index(ws) % 3 == 0 if f == "bitstamp" else STRESS.index(ws) % 2 == 1
    return {"kraken": ws in (t(7, 22), t(7, 23)), "coinbase": ws == t(7, 23), "bitstamp": ws != t(14, 23)}[f]


def fixture(d: str, spec=window.WEEKEND_STRATE_SPEC) -> tuple:
    paths = [os.path.join(d, x) for x in ("control.jsonl", "journal.jsonl", "raw.jsonl")]

    def read_fn(s, ts):
        if not panne(s.flux_id, int(ts) // H * H):
            return frozen_reading(s.flux_id, ts)
        return Reading(flux_id=s.flux_id, kind=s.kind, endpoint=s.endpoint, fetch_ts=ts,
                       currency=s.currency, status=Status.PANNE_HTTP, http_status=401)
    for b in BLOCS:
        clock = [float(b[0])] + [x for ws in b for x in (ws + 1.0, ws + H - DELTA)]
        collector.collect([BY_ID[f] for f in SKELETON], *paths, n_windows=len(b), w=H,
                          sigma_by_class=sbc_huge(), tau_classe=_taumap(TAU), strate_spec=spec,
                          now_fn=FakeClock(clock), sleep_fn=lambda s: None, read_fn=read_fn)
    return paths[0], paths[1]


def section(txt: str) -> list:
    """Lignes de la section, sans la clôture ; section absente : [] (le test échoue, jamais ERROR)."""
    i = txt.find("[SENSIBILITÉ]")
    return txt[i:].splitlines()[:-1] if i >= 0 else []


def cellule(blk) -> str:
    """Ligne attendue, écrite depuis une sortie de r1.recompute_from_journal, jamais depuis le rendu."""
    q = (f"queue exacte P(K ≥ K_obs | Bin(n, P̂_more)) = {blk['queue_binomiale_P_K_ge_Kobs']}"
         if blk["queue_exacte_applicable"] else "queue dégénérée (P̂_more ∈ {0,1})")
    z = f"z = {blk['z']}" if blk["z"] is not None else (
        f"z non publié (garde §5.4 : n·P̂_more·(1−P̂_more) < 10) ; {q}")
    return (f"n = {blk['n']} ; K = {blk['K']} ; P̂_more = {blk['P_more']} ; {z} ; "
            f"drapeau 1 = {blk['flag_historique_insuffisant']}")


class TestSensibilite(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2sens_")
        self.c, self.j = fixture(self.d)

    def table(self, c, j, txt, ranges, segment=None, strates=("calme", "stress")) -> tuple:
        """Cellules = r1.recompute_from_journal (avec, puis sans plages ; même segment) ; écart recalculé."""
        ex, inc = (r1.recompute_from_journal(c, j, exclude_ranges=rg, segment=segment)["strates"]
                   for rg in (ranges, ()))
        sens = section(txt)
        for st in strates:
            e, i = ex[st], inc[st]
            self.assertIn(f"  {st:8} {'exclue (principale)':22} : {cellule(e)}", sens)
            self.assertIn(f"  {st:8} {'incluse (sensibilité)':22} : {cellule(i)}", sens)
            if e["z"] is None or i["z"] is None:
                self.assertIn(f"  {st:8} écart de z : non calculable (z non publié ou strate absente d'une "
                              "variante)", sens)
                continue
            with localcontext() as ctx:
                ctx.prec = 50
                dz = +(i["z"] - e["z"])
            self.assertIn(f"  {st:8} écart de z = {dz if dz else 0}", sens)
        return ex, inc

    def recompte(self, ranges, segment=None) -> dict:
        """{samedi : (exclue, incluse)} : window_close distincts de sam. et dim. (datetime.weekday), plages
        fermées sur window_start, segment [t0 ; n-ième fenêtre distincte ≥ t0, + w) ; incluse sans plages."""
        with open(self.c, encoding="utf-8") as f:
            ws = {o["window_start"] for o in map(json.loads, f) if o.get("record") == "window_close"}
        if segment:
            fin = sorted(x for x in ws if x >= segment["t0"])[segment["n_fixe"] - 1] + H
            ws = {x for x in ws if segment["t0"] <= x < fin}
        out: dict = {}
        for x in ws:
            dt = datetime.fromtimestamp(x, timezone.utc)
            if dt.weekday() >= 5:
                sam = (dt - timedelta(days=dt.weekday() - 5)).date()
                e, i = out.get(sam, (0, 0))
                out[sam] = (e + (not any(a <= x <= b for a, b in ranges)), i + 1)
        return out

    def week_ends(self, txt, ranges, segment=None) -> list:
        rc, sens = self.recompte(ranges, segment), section(txt)
        for sam, (e, i) in rc.items():
            a = int(datetime(sam.year, sam.month, sam.day, tzinfo=timezone.utc).timestamp())
            self.assertIn(f"    week-end {sam} [{a} ; {a + 2 * 86400}) : complet = {PLEIN} fenêtres = "
                          f"{PLEIN} h 00 min ; exclue {e} = {e} h 00 min ; incluse {i} = {i} h 00 min ; "
                          f"retirées par la plage {i - e}", sens)
        self.assertEqual(sum(ln.startswith("    week-end ") for ln in sens), len(rc))
        tot, par = ([sum(f(v[k]) for v in rc.values()) for k in (0, 1)]
                    for f in (lambda n: n == PLEIN, lambda n: 0 < n < PLEIN))
        self.assertIn(f"    en totalité : exclue {tot[0]}, incluse {tot[1]} ; partiellement : exclue "
                      f"{par[0]}, incluse {par[1]} ; retirés en totalité par la plage : "
                      f"{sum(not v[0] for v in rc.values())}", sens)
        return sorted(rc.values())

    def test_table_cellules_ecart_pools_etiquettes(self):
        """C-3, C-4, C-5 : stress, z publié dans les deux variantes ; calme sous la garde, queue exacte ;
        bitstamp hors du pool calme de la variante exclue seule (D1 b, mécanique). Rougit si : variantes
        inversées ; colonne manquante ; écart faux (signe, précision) ; incluse = exclue ; pool de la variante
        gelé ou non imprimé ; étiquette réécrite ; section imprimée sans option."""
        txt = report.render_report(self.c, self.j, exclude_ranges=[RA, RB])
        ex, inc = self.table(self.c, self.j, txt, [RA, RB])
        self.assertTrue(all(b["stress"]["z"] is not None for b in (ex, inc)))           # C-3, mesuré
        self.assertTrue(all(b["calme"]["queue_exacte_applicable"] for b in (ex, inc)))
        self.assertNotEqual(ex["stress"]["z"], inc["stress"]["z"])
        pools = [list(b["calme"]["per_source"]) for b in (ex, inc)]
        self.assertNotEqual(*pools)
        self.assertEqual([ln for ln in section(txt) if "pool d'analyse D1 : " in ln], [
            f"  calme    pool d'analyse D1 : exclue {pools[0]} ; incluse {pools[1]} (diffèrent)"])
        for lib in ("sensibilité — biaisée vers le haut par construction ; documente l'exclusion D5 ; pas un "
                    "estimateur alternatif", "motif de l'exclusion (harnais dégradé, ADR-0025) : causalité "
                    "non établie"):
            self.assertEqual(txt.count(lib), 1)
        self.assertNotIn("[SENSIBILITÉ]", report.render_report(self.c, self.j))

    def test_forme_j28_cli_segment_n_fixe_et_plages(self):
        """C-7 : --segment-from, --segment-n-fixe et deux --exclude-window-start-range, processus neuf :
        sortie = API + « \\n » ; la variante incluse garde le segment. Rougit si : variante incluse sur le
        journal entier ou sous un segment recalculé ; option non transmise."""
        args = ["--segment-from", SEG["t0"], "--segment-n-fixe", SEG["n_fixe"]]
        for a, b in (RA, RB):
            args += ["--exclude-window-start-range", a, b]
        p = subprocess.run([sys.executable, "-B", "-m", "shogen_s2.report", self.d, *map(str, args)],
                           cwd=HARNESS, capture_output=True)
        txt = report.render_report(self.c, self.j, exclude_ranges=[RA, RB], segment=SEG)
        self.assertEqual((p.returncode, p.stdout), (0, f"{txt}\n".encode()))
        self.table(self.c, self.j, txt, [RA, RB], SEG)
        self.assertEqual(self.week_ends(txt, [RA, RB], SEG), [(0, 1), (1, 6), (PLEIN, PLEIN)])
        for x in ("\n  définition d'écart (10 §5.2 ; r1.classify_ecart)", "\n  date de la partition, axe"):
            self.assertEqual(txt.count(x), 1)                                  # blocs 3 et 6 (B-b)

    def test_plage_sans_effet_variantes_egales_ecart_0(self):
        """C-5 (iv) : une plage hors campagne ne retire rien : lignes exclue et incluse égales, écart 0,
        retirées 0 (B-a2). Rougit si : écart imprimé « 0E-49 » ou non nul ; table omise quand la plage ne
        retire rien."""
        txt = report.render_report(self.c, self.j, exclude_ranges=[(t(1, 0), t(1, 5))])
        sens = section(txt)
        for st in ("calme", "stress"):
            self.assertEqual(*[[ln.split(" : ", 1)[1] for ln in sens if ln.startswith(f"  {st:8} {v}")]
                               for v in ("exclue", "incluse")])
        self.assertIn("  stress   écart de z = 0", sens)
        self.assertEqual(self.week_ends(txt, [(t(1, 0), t(1, 5))]), [(3, 3), (6, 6), (PLEIN, PLEIN)])

    def test_couverture_week_ends_recomptee(self):
        """ADR-0025 déc. 4, C-2 : 08-08 complet, 08-15 partiel (5 retirées), 08-22 retiré en totalité ;
        heures = fenêtres × w, w = 3600 s de run_params. Rougit si : complet codé 2880 ou durée à w = 60 ;
        doublons de la reprise comptés ; borne de week-end fausse ; variantes inversées ; catégories
        fausses."""
        txt = report.render_report(self.c, self.j, exclude_ranges=[RA, RB])
        self.assertEqual(self.week_ends(txt, [RA, RB]), [(0, 3), (1, 6), (PLEIN, PLEIN)])

    def test_mono_strate_sans_week_end_ni_exception(self):
        """C-2 : calendrier mono-strate : table de sa seule strate, couverture « non applicable », jamais une
        exception. Rougit si : strates d'un calendrier weekend_utc supposées ; week-ends cherchés sur une
        spec single."""
        c, j = fixture(tempfile.mkdtemp(prefix="s2sens1_"), spec=window.SINGLE_STRATE_SPEC)
        txt = report.render_report(c, j, exclude_ranges=[RA, RB])
        self.table(c, j, txt, [RA, RB], strates=("calme",))
        self.assertEqual(sum("(principale)" in ln for ln in section(txt)), 1)
        self.assertIn("  couverture par week-end : non applicable (calendrier mono-strate)", section(txt))

    def test_queue_degeneree_fixture_d_exclusion(self):
        """Garde §5.4 à P̂_more = 0 dans les deux variantes (fixture de test_exclusion, [w2 ; w4]) : « queue
        dégénérée », jamais une queue vide. Rougit si : branche dégénérée imprimée comme une queue exacte."""
        c, j = build_fixture(tempfile.mkdtemp(prefix="s2sens0_"))
        self.table(c, j, report.render_report(c, j, exclude_ranges=[PLAGE]), [PLAGE])


if __name__ == "__main__":
    unittest.main()
