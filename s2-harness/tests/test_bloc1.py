"""Lot B-SEG-2 (ADR-0028 D5, D6 iv ; SHOGEN-EXCL-COMPTE-1, SHOGEN-NEG-EPOCH-1, HS2-05) : bloc 1 du rendu.
Sous-lot 2a : dates de campagne sur le journal entier ; segment, « aucun » sans option ; par plage, bornes par
type et retraits par strate et par type, puis l'union. Sous-lot 2b : epoch négatif (ValueError à l'API, rc 2 à
la CLI), bloc 5, portée des run_params. Fixture de l'exclusion + poser (D5). Chaque test nomme la mutation
qui le rougit."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest

from shogen_s2 import collector, records, report, window
from tests.test_collector import (BY_ID, DELTA, SKELETON, TAU, W, FakeClock, _taumap, frozen_read_fn,
                                  sbc_huge)
from tests.test_exclusion import HARNESS, WS, build_fixture, comptes_outil, poser, recompte_independant
from tests.test_segment import HOTES, POINTS, WS120, fixture_w120

A, B = WS[2], WS[4]                   # plage D5 de la fixture : w2 calme, w3 et w4 stress
H = len(HOTES)                        # poser : une sonde asn_attribution par hôte et par instant
FEN, ASS = "fenêtres distinctes (window_close)", "seule (assiette : ligne segment) :"
UNI, EXC = "plage(s), union (assiette : ligne segment) :", "— SHOGEN-EXCL-COMPTE-1"
CAMP = "fenêtres distinctes au journal (window_close, avant segment et exclusion)"


def cli(d, *args):
    """Chemin SERVI (RUNBOOK §9 e), processus neuf : (code de retour, stdout, stderr)."""
    p = subprocess.run([sys.executable, "-B", "-m", "shogen_s2.report", d, *map(str, args)], cwd=HARNESS,
                       capture_output=True)
    return p.returncode, p.stdout, p.stderr


def ligne(txt: str, cle: str) -> list:
    """Valeurs des lignes du bloc 1 à la clé `cle`, dans l'ordre."""
    b1 = txt.split("[BLOC 2]")[0].splitlines()
    return [ln.split(" = ", 1)[1] for ln in b1 if ln.startswith(f"  {cle:24} = ")]


class TestBloc1(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2bloc1_")
        self.c, self.j = build_fixture(self.d)
        poser(self.d, (A - 1, A, B, B + 59, B + 60))

    def test_plage_bornes_par_type_et_retraits_par_strate_et_type(self):
        """[w2 ; w4] : ts et harness_ts sur [A ; B + w) ; retirés calme 1, stress 2, 3 × H sondes, 3 horloges,
        égaux aux deux voies du test nommé rejouées sur fixture (C-2 du cp-1) ; CLI = API. Rougit si : strate
        confondue ; type oublié ou interverti ; B sans + w ; ligne d'union absente."""
        txt, iso = report.render_report(self.c, self.j, exclude_ranges=[(A, B)]), report._iso_utc
        self.assertEqual(ligne(txt, "exclusion_ts_harness_ts"), [
            f"[{A} ; {B + W}) = [{iso(A)} ; {iso(B + W)}) semi-ouvert : asn_attribution (ts), clock_check "
            f"(harness_ts), w = {W} s de run_params — ADR-0028 D5"])
        cpt = f"{FEN} calme 1, stress 2 ; asn_attribution {3 * H} ; clock_check 3"
        self.assertEqual(ligne(txt, "exclusion_retraits"), [f"[{A} ; {B}] {ASS} {cpt}"])
        self.assertEqual(ligne(txt, "exclusion_retraits_union"), [f"1 {UNI} {cpt} {EXC}"])
        voie = {"window_close": 3, "asn_attribution": 3 * H, "clock_check": 3}
        self.assertEqual([f(self.c, A, B, W) for f in (comptes_outil, recompte_independant)], [voie, voie])
        self.assertEqual(cli(self.d, "--exclude-window-start-range", A, B)[:2], (0, f"{txt}\n".encode()))

    def test_plages_chevauchantes_chaque_plage_seule_puis_union(self):
        """[w2 ; w4] et [w1 ; w3] : chaque plage seule (ordre trié), puis l'union comptée une fois ; la somme
        dépasse l'union (C-4 i). Rougit si : union = somme des plages ; plage comptée après une autre."""
        txt = report.render_report(self.c, self.j, exclude_ranges=[(A, B), (WS[1], WS[3])])
        self.assertEqual(ligne(txt, "exclusion_retraits"), [
            f"[{WS[1]} ; {WS[3]}] {ASS} {FEN} calme 2, stress 1 ; asn_attribution {2 * H} ; clock_check 3",
            f"[{A} ; {B}] {ASS} {FEN} calme 1, stress 2 ; asn_attribution {3 * H} ; clock_check 3"])
        self.assertEqual(ligne(txt, "exclusion_retraits_union"), [
            f"2 {UNI} {FEN} calme 2, stress 2 ; asn_attribution {4 * H} ; clock_check 5 {EXC}"])

    def test_plage_vide_comptes_a_zero_visibles_rc0(self):
        """Plage avant la campagne : aucun enregistrement dedans, lignes de la plage et de l'union à 0, rc 0
        (C-4 v). Rougit si : ligne omise quand tout est à 0 ; plage vide refusée."""
        a, b = WS[0] - 10 * W, WS[0] - W
        rc, out, _err = cli(self.d, "--exclude-window-start-range", a, b)
        self.assertEqual(rc, 0)
        zero = f"{FEN} calme 0, stress 0 ; asn_attribution 0 ; clock_check 0"
        self.assertEqual(ligne(out.decode(), "exclusion_retraits"), [f"[{a} ; {b}] {ASS} {zero}"])
        self.assertEqual(ligne(out.decode(), "exclusion_retraits_union"), [f"1 {UNI} {zero} {EXC}"])

    def test_dates_de_campagne_avant_filtre_et_retraits_du_segment(self):
        """Segment [w1 ; w4) et plage [w3 ; w5] : dates de campagne au journal entier (6 fenêtres distinctes
        malgré les doublons), identiques sans option ; retraits du segment ; plage comptée sur l'assiette du
        segment ; (e) : started_utc = dernier démarrage (B + w, hors segment), portée déclarée. Rougit si :
        dates après filtre ; doublons comptés ; première et dernière inversées ; plage comptée sur le journal
        entier ; « segment = aucun », portée ou segment_retraits absents ; « aucun » aussi sous segment ;
        union comptée hors de l'assiette du segment (G2 de B-SEG-2)."""
        iso = report._iso_utc
        sans = report.render_report(self.c, self.j)
        txt = report.render_report(self.c, self.j, segment={"t0": WS[1], "t_fin": B},
                                   exclude_ranges=[(WS[3], WS[5])])
        for t in (sans, txt):
            self.assertEqual(ligne(t, "campagne_fenetres"), [
                f"6 {CAMP} : première {WS[0]} = {iso(WS[0])} ; "
                f"dernière {WS[5]} = {iso(WS[5])} (window_start) — HS2-05"])
            self.assertEqual(ligne(t, "portee_run_params"), [
                "journal entier, jamais segmenté ni exclu (§E) : run_params_demarrages = tous les "
                "démarrages ; started_utc, n_windows_demande = dernier démarrage (HS2-05)"])
        self.assertEqual(ligne(txt, "started_utc"), [iso(B + W)])
        self.assertEqual(ligne(sans, "segment"), ["aucun (journal entier) — ADR-0028 D4"])
        self.assertEqual(len(ligne(txt, "segment")), 1)          # sous segment : [t0 ; t_fin) seule
        self.assertEqual(ligne(txt, "segment_retraits"), [
            f"hors segment : {FEN} calme 1, stress 2 ; asn_attribution {3 * H} ; clock_check 4 "
            "— ADR-0028 D4"])
        self.assertEqual(ligne(txt, "exclusion_retraits"), [
            f"[{WS[3]} ; {WS[5]}] {ASS} {FEN} calme 0, stress 1 ; asn_attribution 0 ; clock_check 0"])
        self.assertEqual(ligne(txt, "exclusion_retraits_union"), [
            f"1 {UNI} {FEN} calme 0, stress 1 ; asn_attribution 0 ; clock_check 0 {EXC}"])

    def test_bornes_ts_harness_ts_w_lu_de_run_params(self):
        """w = 120 s (fixture du G2 de B-SEG-1) : [A ; B + 120) et les retraits sur cette borne. Rougit si :
        + 60 codé en dur."""
        a, b = WS120[2], WS120[3]
        c, j = fixture_w120(tempfile.mkdtemp(prefix="s2bloc1w_"), (a - 1, a + 90, b + 60, b + 119, b + 120))
        txt, iso = report.render_report(c, j, exclude_ranges=[(a, b)]), report._iso_utc
        self.assertEqual(ligne(txt, "exclusion_ts_harness_ts"), [
            f"[{a} ; {b + 120}) = [{iso(a)} ; {iso(b + 120)}) semi-ouvert : asn_attribution (ts), "
            "clock_check (harness_ts), w = 120 s de run_params — ADR-0028 D5"])
        self.assertEqual(ligne(txt, "exclusion_retraits"), [
            f"[{a} ; {b}] {ASS} {FEN} calme 0, stress 2 ; asn_attribution {3 * H} ; clock_check 3"])

    def test_journal_sans_fenetre_dates_de_campagne_sans_lever(self):
        """Un démarrage sans fenêtre (0 marqueur) : la ligne sort, sans première ni dernière. Rougit si : la
        première fenêtre est lue sur une liste vide ; sous plage, compte de fenêtres vide au lieu d'un 0
        visible (G2 de B-SEG-2)."""
        d = tempfile.mkdtemp(prefix="s2bloc1z_")
        c, j, raw = (os.path.join(d, n) for n in ("control.jsonl", "journal.jsonl", "raw.jsonl"))
        collector.collect([BY_ID[f] for f in SKELETON], c, j, raw, n_windows=0, sigma_by_class=sbc_huge(),
                          tau_classe=_taumap(TAU), strate_spec=window.WEEKEND_STRATE_SPEC,
                          now_fn=FakeClock([float(WS[0])]), sleep_fn=lambda s: None, read_fn=frozen_read_fn)
        open(j, "a", encoding="utf-8").close()
        self.assertEqual(ligne(report.render_report(c, j), "campagne_fenetres"), [
            f"0 {CAMP} — HS2-05"])
        txt = report.render_report(c, j, exclude_ranges=[(WS[0] - W, WS[0] + W)])
        self.assertEqual(ligne(txt, "exclusion_retraits_union"), [
            f"1 {UNI} {FEN} 0 (aucune fenêtre au journal) ; asn_attribution 0 ; clock_check 1 {EXC}"])

    def test_premiere_et_derniere_fenetre_hors_ordre_du_journal(self):
        """Premières occurrences écrites hors ordre (w3-w5, puis w0-w2 ; collecteur réel, horloge scriptée) :
        première = min, dernière = max des window_start (G2 de B-SEG-2). Rougit si : ordre d'écriture lu."""
        paths = [os.path.join(tempfile.mkdtemp(prefix="s2bloc1o_"), n)
                 for n in ("control.jsonl", "journal.jsonl", "raw.jsonl")]
        for wins in (WS[3:6], WS[0:3]):
            clock = [float(wins[0])] + [t for b in wins for t in (b + 1.0, b + W - DELTA)]
            collector.collect([BY_ID[f] for f in SKELETON], *paths, n_windows=len(wins),
                              sigma_by_class=sbc_huge(), tau_classe=_taumap(TAU),
                              strate_spec=window.WEEKEND_STRATE_SPEC,
                              now_fn=FakeClock(clock), sleep_fn=lambda s: None, read_fn=frozen_read_fn)
        self.assertEqual(ligne(report.render_report(*paths[:2]), "campagne_fenetres"), [
            f"6 {CAMP} : première {WS[0]} = {report._iso_utc(WS[0])} ; dernière {WS[5]} = "
            f"{report._iso_utc(WS[5])} (window_start) — HS2-05"])

    def test_epoch_negatif_rc2_cli_et_valueerror_api(self):
        """SHOGEN-NEG-EPOCH-1 (Q-G2-5), étendu au segment ((d), G2 de B-SEG-1) : CLI rc 2, message sur stderr,
        stdout vide ; API : ValueError aux quatre points d'entrée et dans l'outil ; n fixe négatif : rc 1 (C-4
        iv : n n'est pas un epoch). Rougit si : rc 1 au lieu de 2 ; segment négatif accepté (CLI ou API) ;
        plage négative acceptée à l'API ; -0,5 tronqué en 0 ; n fixe refusé comme un epoch (rc 2)."""
        for args in (("--segment-from", -5, "--segment-to", B), ("--segment-from", 0, "--segment-to", -1),
                     ("--exclude-window-start-range", -5, 10), ("--exclude-window-start-range", 5, -1)):
            rc, out, err = cli(self.d, *args)
            self.assertEqual((rc, out), (2, b""), args)
            self.assertIn(b"SHOGEN-NEG-EPOCH-1", err)
        self.assertEqual(cli(self.d, "--segment-from", WS[0], "--segment-n-fixe", -1)[:2], (1, b""))
        for kw in ({"exclude_ranges": [(-5, 10)]}, {"segment": {"t0": -5, "t_fin": B}},
                   {"segment": {"t0": -5, "n_fixe": 2}}, {"segment": {"t0": 0, "t_fin": -1}}):
            for f in POINTS:
                with self.assertRaises(ValueError, msg=(f.__qualname__, kw)):
                    f(self.c, self.j, **kw)
        for r in ((-0.5, 10), (0, -0.5)):         # int() tronquerait -0,5 en 0 : contrôle avant
            with self.assertRaises(ValueError, msg=r):
                records.exclusion_ranges([r])

    def test_epoch_zero_accepte_t0_fractionnaire_refuse(self):
        """Bord de SHOGEN-NEG-EPOCH-1 (G2 de B-SEG-2) : 0 n'est pas négatif, accepté à la CLI et à l'API ;
        t0 = -0,5 refusé aux quatre points. Rougit si : <= au lieu de < (CLI, plage, segment) ; t0 tronqué."""
        for args in (("--exclude-window-start-range", 0, 5), ("--segment-from", 0, "--segment-to", B)):
            self.assertEqual(cli(self.d, *args)[0], 0, args)
        self.assertEqual(records.exclusion_ranges([(0, 0)]), [(0, 0)])
        for f in POINTS:
            f(self.c, self.j, segment={"t0": 0, "t_fin": B})
            for seg in ({"t0": -0.5, "t_fin": B}, {"t0": -0.5, "n_fixe": 2}):
                with self.assertRaisesRegex(ValueError, "SHOGEN-NEG-EPOCH-1", msg=(f.__qualname__, seg)):
                    f(self.c, self.j, segment=seg)

    def test_bloc5_sondes_toutes_retirees_message_vrai(self):
        """(c), G2 de B-SEG-1 : [w0 ; w5 − 1] retire toutes les sondes ; le bloc 5 le dit, avec ses deux
        comptes ; journal sans sonde : message d'origine. Rougit si : ancien message gardé après un filtre
        total ; message neuf sur un journal sans sonde."""
        txt = report.render_report(self.c, self.j, exclude_ranges=[(WS[0], WS[5] - 1)])
        self.assertIn(f"retenu pour les hôtes du pool — {5 * H} au journal, 0 retenus par le filtre", txt)
        self.assertNotIn("collect_asn non lancé", txt)
        sans = report.render_report(*build_fixture(tempfile.mkdtemp(prefix="s2bloc1n_")))
        self.assertIn("aucun enregistrement asn_attribution au journal (collect_asn non lancé", sans)
        self.assertNotIn("retenu pour les hôtes du pool", sans)


if __name__ == "__main__":
    unittest.main()
