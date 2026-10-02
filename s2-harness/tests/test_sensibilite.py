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

from shogen_s2 import collector, r1, r2, report, window
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


def fixture(d: str, spec=window.WEEKEND_STRATE_SPEC, blocs=BLOCS, w=H, en_panne=panne) -> tuple:
    """Blocs, w et pannes paramétrés (revue G2, C-1 à C-5) ; défauts : fixture de conception."""
    paths = [os.path.join(d, x) for x in ("control.jsonl", "journal.jsonl", "raw.jsonl")]

    def read_fn(s, ts):
        if not en_panne(s.flux_id, int(ts) // w * w):
            return frozen_reading(s.flux_id, ts)
        return Reading(flux_id=s.flux_id, kind=s.kind, endpoint=s.endpoint, fetch_ts=ts,
                       currency=s.currency, status=Status.PANNE_HTTP, http_status=401)
    for b in blocs:
        clock = [float(b[0])] + [x for ws in b for x in (ws + 1.0, ws + w - DELTA)]
        collector.collect([BY_ID[f] for f in SKELETON], *paths, n_windows=len(b), w=w,
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


def attendu_we(c: str, ranges) -> list:
    """Revue G2 (C-1) : lignes de couverture attendues, recomptées en bibliothèque standard (datetime) depuis
    control.jsonl : suites maximales de jours de stress_weekdays, fenêtres distinctes, plages fermées."""
    with open(c, encoding="utf-8") as f:
        objs = [json.loads(x) for x in f]
    rp = [o for o in objs if o["record"] == "run_params"][-1]
    w, jours, un, cpt = int(rp["w"]), set(rp["strate_calendar"]["stress_weekdays"]), timedelta(days=1), {}
    pl = "la plage" if len(ranges) == 1 else f"les {len(ranges)} plages"              # SENS-PLAGES-2
    for x in {o["window_start"] for o in objs if o["record"] == "window_close"}:
        a = b = datetime.fromtimestamp(x, timezone.utc).date()
        if a.weekday() in jours:
            while (a - un).weekday() in jours:
                a -= un
            while (b + un).weekday() in jours:
                b += un
            e, i = cpt.get((a, b), (0, 0))
            cpt[a, b] = (e + (not any(lo <= x <= hi for lo, hi in ranges)), i + 1)
    def dur(s: int) -> str:
        return "%d h %02d min" % (s // 3600, s % 3600 // 60) + (" %02d s" % (s % 60) if s % 60 else "")
    out = []
    for (a, b), (e, i) in sorted(cpt.items()):
        A = int(datetime(a.year, a.month, a.day, tzinfo=timezone.utc).timestamp())
        B = A + ((b - a).days + 1) * 86400
        p = (B - A) // w
        out.append(f"    week-end {a} [{A} ; {B}) : complet = {p} fenêtres = {dur(p * w)} ; exclue {e} = "
                   f"{dur(e * w)} ; incluse {i} = {dur(i * w)} ; retirées par {pl} {i - e}")
    return out


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
        pl = "la plage" if len(ranges) == 1 else f"les {len(ranges)} plages"          # SENS-PLAGES-2
        for sam, (e, i) in rc.items():
            a = int(datetime(sam.year, sam.month, sam.day, tzinfo=timezone.utc).timestamp())
            self.assertIn(f"    week-end {sam} [{a} ; {a + 2 * 86400}) : complet = {PLEIN} fenêtres = "
                          f"{PLEIN} h 00 min ; exclue {e} = {e} h 00 min ; incluse {i} = {i} h 00 min ; "
                          f"retirées par {pl} {i - e}", sens)
        self.assertEqual(sum(ln.startswith("    week-end ") for ln in sens), len(rc))
        tot, par = ([sum(f(v[k]) for v in rc.values()) for k in (0, 1)]
                    for f in (lambda n: n == PLEIN, lambda n: 0 < n < PLEIN))
        self.assertIn(f"    en totalité : exclue {tot[0]}, incluse {tot[1]} ; partiellement : exclue "
                      f"{par[0]}, incluse {par[1]} ; retirés en totalité par {pl} : "
                      f"{sum(not v[0] for v in rc.values())}", sens)
        self.assertIn("    non couverts (0 fenêtre dans les deux variantes, entre la première et la dernière "
                      "fenêtre de l'assiette) : 0", sens)                               # G2 C-5
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
        for x in ("\n  définition d'écart (10 §5.2 ; τ relatif : ADR-0020 déc. 2, ADR-0022 ; r1.classify_ecart)",
                  "\n  date de la partition, axe"):
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


class TestSensibiliteG2(unittest.TestCase):
    """Revue G2 du lot B (C-1 à C-5) : trous d'oracle, week-end calendaire sans fenêtre. Chaque test nomme le
    mutant du réviseur qui le rougit (revue G2 du lot B, §8)."""

    def test_g2_couverture_calendriers_et_w(self):
        """C-1 : stress_weekdays [6, 0] (enjambe la semaine), [4, 5, 6], [2], puis [5, 6] à w = 90 s
        (« SS s »). Rougit si : jours {5, 6} codés (MR03) ; week-end coupé au lundi (MR11) ; secondes
        omises (MR01) ; stress_weekdays codé dans l'en-tête (MR13)."""
        cas = (([6, 0], H, range(t(8, 20), t(11, 4), H), [(t(10, 10), t(10, 12))]),
               ([4, 5, 6], H, range(t(6, 22), t(10, 2), H), [(t(8, 0), t(8, 23))]),
               ([2], 1800, range(t(11, 22), t(13, 2), 1800), [(t(11, 22), t(11, 23))]),
               ([5, 6], 90, range(t(8, 23), t(9, 1), 90), [(t(8, 23) + 1800, t(8, 23) + 1980)]))
        for jours, w, bloc, rg in cas:
            spec = dict(window.WEEKEND_STRATE_SPEC, stress_weekdays=jours)
            c, j = fixture(tempfile.mkdtemp(prefix="s2g2c1_"), spec, [bloc], w, lambda f, ws: False)
            sens, att = section(report.render_report(c, j, exclude_ranges=rg)), attendu_we(c, rg)
            self.assertIn(f"  couverture par week-end (fenêtres « stress », stress_weekdays = "
                          f"{sorted(jours)} UTC ; w = {w} s de run_params ; durée = fenêtres × w) :", sens)
            self.assertEqual([ln for ln in sens if ln.startswith("    week-end ")], att)
        self.assertIn("exclue 77 = 1 h 55 min 30 s ; incluse 80 = 2 h 00 min", att[0])   # w = 90 s

    def test_g2_non_applicable_absente_et_mono_nommee(self):
        """C-2 : stress_weekdays vide ou plein : « non applicable », strate absente des deux variantes, écart
        non calculable ; mono-strate nommée « unique ». Rougit si : garde vide ou plein affaiblie (MR04 ;
        MR05, boucle sans fin) ; message permuté (MR15) ; « absente » réécrit (MR09) ; strate codée (MR08)."""
        rg, sain = [(t(7, 22), t(7, 23))], (lambda f, ws: False)
        for jours, absente in (([], "stress"), (list(range(7)), "calme")):
            spec = dict(window.WEEKEND_STRATE_SPEC, stress_weekdays=jours)
            c, j = fixture(tempfile.mkdtemp(prefix="s2g2c2_"), spec, [range(t(7, 20), t(8, 4), H)], H, sain)
            sens = section(report.render_report(c, j, exclude_ranges=rg))
            self.assertIn("  couverture par week-end : non applicable (stress_weekdays sans borne de "
                          "week-end)", sens)
            for v in ("exclue (principale)", "incluse (sensibilité)"):
                self.assertIn(f"  {absente:8} {v:22} : absente (0 fenêtre retenue)", sens)
            self.assertIn(f"  {absente:8} écart de z : non calculable (z non publié ou strate absente "
                          "d'une variante)", sens)
        spec = {"kind": "single", "strate": "unique", "note": "mono-strate nommée (revue G2)"}
        c, j = fixture(tempfile.mkdtemp(prefix="s2g2c2m_"), spec, [range(t(7, 20), t(8, 4), H)], H, sain)
        sens = section(report.render_report(c, j, exclude_ranges=rg))
        self.assertEqual([ln.split()[0] for ln in sens if "(principale)" in ln], ["unique"])
        self.assertIn("  couverture par week-end : non applicable (calendrier mono-strate)", sens)

    def test_g2_bloc6_k_sur_n(self):
        """C-3 : un seul hôte du pool sondé : « 1 / 3 hôtes du pool ». Rougit si : N = k (MR06)."""
        c, j = build_fixture(tempfile.mkdtemp(prefix="s2g2c3_"))
        ok, ts = {"status": "ok", "asn_ripestat": 64600, "asn_cymru": 64600}, float(PLAGE[0] - 30)
        r2.collect_asn([BY_ID["coinbase"]], c, resolve_fn=lambda h, r: ok, now_fn=lambda: ts)
        iso = report._iso_utc(ts)
        self.assertIn("  date de la partition, axe ASN (ADR-0026 déc. 1 ; HS2-07) = relevé asn_attribution "
                      f"retenu (dernier par hôte, après filtre de lecture) : min {ts} = {iso} ; max {ts} = "
                      f"{iso} ; 1 / 3 hôtes du pool — descriptif seulement (ADR-0028 annexe D.5)",
                      report.render_report(c, j).splitlines())

    def test_g2_pool_cas_a_entre_variantes(self):
        """C-4 : bitstamp n'a de lecture ok que dans RA : hors du pool du segment dans la variante exclue
        (D1 cas a), au pool des deux strates dans l'incluse. Rougit si : pool de base de la variante = pool
        d'analyse principal (MR07)."""
        c, j = fixture(tempfile.mkdtemp(prefix="s2g2c4_"), blocs=BLOCS[:2],
                       en_panne=lambda f, ws: f == "bitstamp" and not RA[0] <= ws <= RA[1])
        txt = report.render_report(c, j, exclude_ranges=[RA])
        ex, inc = TestSensibilite.table(self, c, j, txt, [RA])
        self.assertEqual([("bitstamp" in b[s]["per_source"]) for b in (ex, inc) for s in ("calme", "stress")],
                         [False, False, True, True])
        self.assertEqual(sum("pool d'analyse D1 : " in ln for ln in section(txt)), 2)

    def test_g2_week_end_sans_fenetre_visible(self):
        """C-5 : le week-end du 08-15, sans aucune fenêtre entre deux fenêtres de l'assiette, est listé à 0 et
        compté « non couvert ». Rougit si : week-ends calendaires sans fenêtre omis (MR21) ; comptés
        « retirés en totalité par la plage » (MR22)."""
        blocs = [range(t(7, 22), t(10, 2), H), range(t(14, 20), t(15, 0), H), range(t(17, 0), t(17, 4), H),
                 range(t(22, 0), t(22, 3), H)]
        c, j = fixture(tempfile.mkdtemp(prefix="s2g2c5_"), blocs=blocs, en_panne=lambda f, ws: False)
        sens, a = section(report.render_report(c, j, exclude_ranges=[RB])), t(15, 0)
        self.assertIn(f"    week-end 2026-08-15 [{a} ; {a + 2 * 86400}) : complet = {PLEIN} fenêtres = "
                      f"{PLEIN} h 00 min ; exclue 0 = 0 h 00 min ; incluse 0 = 0 h 00 min ; retirées par la "
                      "plage 0", sens)
        self.assertEqual(sens[-2:], [
            "    en totalité : exclue 1, incluse 1 ; partiellement : exclue 0, incluse 1 ; retirés en "
            "totalité par la plage : 1", "    non couverts (0 fenêtre dans les deux variantes, entre la "
            "première et la dernière fenêtre de l'assiette) : 1"])


class TestSensPertes(unittest.TestCase):
    def test_pertes_du_journal_par_plage_et_par_strate(self):
        """SHOGEN-SENS-PERTES-2 : plages [lun. 10 00:00Z ; 05:00Z] (calme) et [sam. 15 04:00Z ; 09:00Z] (stress),
        chacune sur la fin d'un bloc (marqueurs à 00:00, 01:00 et 04:00, 05:00) : 4 fenêtres de grille sans
        marqueur chacune ; lectures retirées du journal : kraken à lun. 01:00Z, coinbase et bitstamp à sam. 05:00Z
        (pool D1 de la variante incluse : 3 flux par strate) ; sous le segment [ven. 7 22:00Z ; lun. 10 03:00Z) :
        1 fenêtre sans marqueur ; C-11 : plage [ven. 7 22:00Z ; 23:00Z], bitstamp absent à 23:00Z mais hors du pool
        D1 de la variante incluse en calme sous ce segment (0 lecture ok) : non compté (R24) ; plage [lun. 10 00:00Z ;
        01:00Z], kraken absent sur la borne haute : compté (R23). Rougit si : fenêtres sans marqueur hors de la plage
        (ou du segment) ; lectures absentes comptées hors des fenêtres à marqueur ; strates confondues ; borne haute
        exclue ; pool autre que D1 ; ligne absente."""
        c, j = fixture(tempfile.mkdtemp(prefix="s2pertes_"))
        retirees = {(t(10, 1), "kraken"), (t(15, 5), "coinbase"), (t(15, 5), "bitstamp"), (t(7, 23), "bitstamp")}
        with open(j, encoding="utf-8") as f:
            lignes = [x for x in f
                      if (lambda o: (o["window_start"], o["flux_id"]))(json.loads(x)) not in retirees]
        with open(j, "w", encoding="utf-8") as f:
            f.writelines(lignes)
        ra, rb = (t(10, 0), t(10, 5)), (t(15, 4), t(15, 9))

        def att(a, b, sc, ss, lc, ls):
            return (f"    [{a} ; {b}] pertes du journal dans la plage : fenêtres de grille sans marqueur calme "
                    f"{sc}, stress {ss} ; lectures absentes des fenêtres à marqueur (pool D1 de la variante "
                    f"incluse) calme {lc}, stress {ls} — SHOGEN-SENS-PERTES-2")
        sens = section(report.render_report(c, j, exclude_ranges=[ra, rb]))
        self.assertEqual([x for x in sens if "SHOGEN-SENS-PERTES-2" in x],
                         [att(*ra, 4, 0, 1, 0), att(*rb, 0, 4, 0, 2)])
        seg = {"t0": t(7, 22), "t_fin": t(10, 3)}
        sens = section(report.render_report(c, j, exclude_ranges=[ra], segment=seg))
        self.assertEqual([x for x in sens if "SHOGEN-SENS-PERTES-2" in x], [att(*ra, 1, 0, 1, 0)])
        rc, rd = (t(7, 22), t(7, 23)), (t(10, 0), t(10, 1))
        sens = section(report.render_report(c, j, exclude_ranges=[rc, rd], segment=seg))
        self.assertEqual([x for x in sens if "SHOGEN-SENS-PERTES-2" in x], [att(*rc, 0, 0, 0, 0), att(*rd, 0, 0, 1, 0)])


if __name__ == "__main__":
    unittest.main()
