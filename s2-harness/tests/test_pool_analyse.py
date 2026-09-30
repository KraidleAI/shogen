"""Lot B0 (ADR-0028 D1) : un flux sans lecture « ok » (statut ok ET prix) dans une strate retenue
sort du pool de cette strate (R1, L&M) ; mort dans toutes les strates retenues, il sort aussi de R2.
Attendus MÉTAMORPHIQUES (C-B0-4) : la règle sur P avec f mort = le code d'avant le lot (`compute_*`,
signatures inchangées) sur P privé de f, jamais lus dans une sortie du code neuf. Fixtures du
collecteur réel (C-B0-3), flux mort pris par indice. Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import hashlib
import os
import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from itertools import count

from shogen_s2 import collector, lm, r1, r2, records, report, window
from shogen_s2.model import Reading, Status
from tests.test_collector import (BY_ID, DELTA, SKELETON, TAU, W, FakeClock, _taumap,
                                  frozen_reading, sbc_huge)
from tests.test_exclusion import PLAGE, build_fixture, cli

MORT, VIFS = SKELETON[0], SKELETON[1:]
WS = [int(datetime(2026, 8, 7, 23, 57, tzinfo=timezone.utc).timestamp()) + i * W
      for i in range(64)]                                     # w0-w2 calme (ven.), w3-w63 stress
# Épingle (CA-13 bis) : sha256 du rendu AVEC l'option [w2 ; w4] de la fixture d'exclusion, arbre ce2f107,
# re-capturé à chaque sous-lot de B-SEG-2 qui ajoute une ligne au bloc 1 (avant : a4dd4c00…537520), puis de B
# (B-a1 : section [SENSIBILITÉ], avant 677b1bfc…422114 ; P2P texte : docs/G1-lot-B-sensibilite.md).
SHA_BASE_AVEC_OPTION = "7a4ff05c297c74aae9825a6d8f108ea24c1c4460cd46dd1807fc88cd2d663734"


class Coupure(Exception):
    """Le harnais meurt pendant une fenêtre : lectures écrites, marqueur absent."""


def collecte(d, n, script, specs=SKELETON, depuis=0):
    """Collecteur réel, horloge scriptée ; script(flux, i) : ok, panne (401), nul (ok sans prix), coupure."""
    def read_fn(spec, ts):
        k = script(spec.flux_id, (int(ts) - WS[0]) // W)
        if k == "coupure":
            raise Coupure(spec.flux_id)
        if k == "ok":
            return frozen_reading(spec.flux_id, ts)
        return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint, fetch_ts=ts,
                       currency=spec.currency,          # forme de sources.read (l.381-394)
                       status=Status.OK if k == "nul" else Status.PANNE_HTTP,
                       http_status=200 if k == "nul" else 401)
    wins = WS[depuis:depuis + n]
    clock = [float(wins[0])] + [t for b in wins for t in (b + 1.0, b + W - DELTA)]
    paths = [os.path.join(d, x) for x in ("control.jsonl", "journal.jsonl", "raw.jsonl")]
    try:
        collector.collect([BY_ID[f] for f in specs], *paths, n_windows=n, sigma_by_class=sbc_huge(),
                          tau_classe=_taumap(TAU), strate_spec=window.WEEKEND_STRATE_SPEC,
                          now_fn=FakeClock(clock), sleep_fn=lambda s: None, read_fn=read_fn)
    except Coupure:
        pass
    return paths[0], paths[1]


def fixture_b(d):
    """f vivant en calme ; en stress (w3-w62), aucune lecture ok RETENUE : w3 ok puis re-collectée
    en panne (last-wins), w4 ok à prix nul, w5-w62 panne, w63 ok orpheline (coupure avant le
    marqueur). Les deux autres flux tombent ensemble aux fenêtres stress impaires (z publié)."""
    def script(f, i):
        if f == MORT:
            return "ok" if i <= 3 or i == 63 else ("nul" if i == 4 else "panne")
        return "coupure" if i == 63 else ("panne" if i >= 3 and i % 2 else "ok")
    collecte(d, 64, script)
    return collecte(d, 1, lambda f, i: "panne" if f == MORT else script(f, i), depuis=3)


def base(c, j, pool, strate=None, ranges=()):
    """Code d'AVANT le lot sur `pool`, marqueurs retenus par l'exclusion, restreints à `strate`."""
    plist, _clock, m = records.parse_control(c)
    p = records.effective_run_params(plist, records.LOAD_BEARING_KEYS + records.R2_LOAD_BEARING_KEYS)
    m = [x for x in records.exclude_window_start_ranges(m, ranges) if strate in (None, x["strate"])]
    rd, (sbc, scf, tau) = r1.parse_journal(j), records.sigma_tau_from_params(p)
    w, nm = int(p["w"]), int(p["n_min_hors_enveloppe"])
    return (r1.compute_r1(m, rd, pool, w, sbc, scf, tau, Decimal(str(p["seuil_historique_valeur"])), nm),
            lm.compute_lm(m, rd, pool, w, sbc, scf, tau, nm),
            r2.compute_r2(m, rd, records.parse_asn(c), pool, w, sbc, scf, tau, p, n_min_horsenv=nm))


def k_nominal(pool) -> str:
    hotes = r2.hosts_of_pool(r2.build_flux_hosts([BY_ID[f] for f in pool]), pool)
    return f"{len(hotes)} sources / {len(pool)} flux"


class TestPoolAnalyse(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2pool_")

    def test_a_flux_mort_partout_hors_r1_lm_r2_aux_quatre_points(self):
        """Cas (a), f en panne HTTP 401 dans les 6 fenêtres. Rougit si : règle désactivée ou omise à
        un des quatre points d'entrée ; N de L&M = len(run_params.pool) ; retrait absent, en trop ou
        mal compté au bloc 1 ; k nominal par strate absent."""
        c, j = collecte(self.d, 6, lambda f, i: "panne" if f == MORT else "ok")
        ref = base(c, j, VIFS)
        self.assertEqual(r1.recompute_from_journal(c, j), ref[0])
        self.assertEqual(lm.recompute_lm_from_journal(c, j), ref[1])
        self.assertEqual(r2.recompute_r2_from_journal(c, j), ref[2])
        sans = os.path.join(self.d, "sans_f")
        os.mkdir(sans)
        c2, j2 = collecte(sans, 6, lambda f, i: "ok", specs=VIFS)   # même collecte, P privé de f
        txt = report.render_report(c, j)
        self.assertEqual(txt.split("[BLOC 3]")[1], report.render_report(c2, j2).split("[BLOC 3]")[1])
        self.assertEqual(txt.count("pool_analyse_retrait"), 2)
        dev = [[x for x in t.splitlines() if "devise_composition" in x]
               for t in (txt, report.render_report(c2, j2))]
        self.assertEqual(dev[0], dev[1])                 # bloc 1 sur le pool d'analyse (C-1 du G2)
        for st in ("calme", "stress"):
            self.assertIn(f"= {MORT} strate « {st} » : ok = 0 / 3 lectures, n = 3 — hors R1 et L&M "
                          "de la strate, cas (a), hors R2 aussi", txt)
            self.assertIn(f"= « {st} » : {k_nominal(VIFS)}", txt)
        self.assertEqual(cli(self.d), (txt + "\n").encode("utf-8"))       # processus neuf

    def test_a_mort_hors_tete_et_hote_partage(self):
        """G2 C-3 : flux mort en fin de pool, deux flux vifs d'un même hôte. Rougit : retrait par
        position dans le pool ; k nominal par strate qui compte les flux au lieu des hôtes."""
        fh = r2.build_flux_hosts(list(BY_ID.values()))
        vifs = sorted(f for f in fh if list(fh.values()).count(fh[f]) == 2)
        c, j = collecte(self.d, 6, lambda f, i: "panne" if f == MORT else "ok", specs=vifs + [MORT])
        self.assertEqual(r1.recompute_from_journal(c, j), base(c, j, vifs)[0])
        self.assertEqual(k_nominal(vifs), f"1 sources / {len(vifs)} flux")
        txt = report.render_report(c, j)
        for st in ("calme", "stress"):
            self.assertIn(f"= « {st} » : {k_nominal(vifs)}", txt)

    def test_b_mort_en_stress_seul_retire_de_cette_strate_seulement(self):
        """Cas (b), sous-lot B0-2. Rougit si : (b) traité comme (a) ; (b) appliqué à R2 ; N de L&M
        laissé à len(run_params.pool) ; drapeau 2 sur un autre z que celui du bloc 3 ; k nominal
        ou N par strate absent ; prédicat ok élargi, last-wins ignoré, orphelines comptées."""
        c, j = fixture_b(self.d)
        asn = count(64512)

        def resolve(host, resolvers):                           # un AS distinct par hôte : drapeau 2 évaluable
            a = next(asn)
            return {"status": "ok", "resolver": resolvers[0], "ip": "192.0.2.1", "ip_secondary": [],
                    "cname_chain": [], "prefix": "192.0.2.0/24", "asn_ripestat": a, "asn_cymru": a,
                    "holder": "TEST"}
        r2.collect_asn([BY_ID[f] for f in SKELETON], c, resolve_fn=resolve, now_fn=lambda: float(WS[0]))
        out1, outlm = r1.recompute_from_journal(c, j), lm.recompute_lm_from_journal(c, j)
        r1m, lmm = {"strates": {}}, {"strates": {}}
        for st, pool in (("calme", SKELETON), ("stress", VIFS)):
            ref = base(c, j, pool, strate=st)
            r1m["strates"][st], lmm["strates"][st] = ref[0]["strates"][st], ref[1]["strates"][st]
            self.assertEqual(out1["strates"][st], r1m["strates"][st])
            self.assertEqual(outlm["strates"][st], lmm["strates"][st])
        self.assertIsNotNone(r1m["strates"]["stress"]["z"])
        out2, ref2 = r2.recompute_r2_from_journal(c, j), base(c, j, SKELETON)[2]
        ref2.pop("drapeau_2")
        self.assertEqual(out2.pop("drapeau_2"), r2.drapeau_2(r1m, ref2["partition"], lmm))
        self.assertEqual(out2, ref2)                            # R2 : cas (a) seul, f y reste
        txt = report.render_report(c, j)
        self.assertEqual(txt.count("pool_analyse_retrait"), 1)
        self.assertIn(f"= {MORT} strate « stress » : ok = 0 / 60 lectures, n = 60 — hors R1 et L&M "
                      "de la strate, cas (b), gardé par R2", txt)
        self.assertIn(f"= « calme » : {k_nominal(SKELETON)}", txt)
        self.assertIn(f"= « stress » : {k_nominal(VIFS)}", txt)
        self.assertRegex(txt, rf"strate « stress » : n = 60 ; Σ mⱼ = \d+ ; N = {len(VIFS)}\n")
        self.assertEqual(cli(self.d), (txt + "\n").encode("utf-8"))

    def test_regle_apres_exclusion_strate_videe_hors_de_s(self):
        """[w0 ; w2] vide la strate calme : S = {stress}, où f n'a aucune lecture ok retenue, donc
        cas (a) ; rien pour la strate vide. Rougit si : règle calculée avant l'exclusion ; strate vide
        comptée dans S ; prédicat ok élargi (w4) ; last-wins ignoré (w3) ; orphelines comptées (w63)."""
        c, j = fixture_b(self.d)
        rg = [(WS[0], WS[2])]
        ref = base(c, j, VIFS, ranges=rg)
        self.assertEqual(r1.recompute_from_journal(c, j, exclude_ranges=rg), ref[0])
        self.assertEqual(lm.recompute_lm_from_journal(c, j, exclude_ranges=rg), ref[1])
        self.assertEqual(r2.recompute_r2_from_journal(c, j, exclude_ranges=rg), ref[2])
        txt = report.render_report(c, j, exclude_ranges=rg)
        self.assertEqual((txt.count("pool_analyse_retrait"), txt.count("k_nominal_strate")), (1, 1))
        self.assertIn("ok = 0 / 60 lectures, n = 60 — hors R1 et L&M de la strate, cas (a)", txt)

    def test_epingle_sans_flux_mort_octets_de_base_avec_option(self):
        """Épingle (CA-13 bis ; re-captures B-SEG-2 : lignes ajoutées au bloc 1) : sans flux mort, le rendu
        AVEC l'option garde les octets épinglés (sans option : test_exclusion iv) ; S vide, aucun retrait.
        Rougit si : ligne de retrait ou de k nominal sans retrait ; S vide lu comme « tout est mort »."""
        c, j = build_fixture(self.d)
        txt = report.render_report(c, j, exclude_ranges=[PLAGE])
        self.assertEqual(hashlib.sha256(txt.encode("utf-8")).hexdigest(), SHA_BASE_AVEC_OPTION)
        self.assertEqual(cli(self.d, PLAGE), (txt + "\n").encode("utf-8"))
        tout = [(PLAGE[0] - 10 * W, PLAGE[1] + 10 * W)]            # toutes les fenêtres exclues
        self.assertEqual(r2.recompute_r2_from_journal(c, j, exclude_ranges=tout),
                         base(c, j, SKELETON, ranges=tout)[2])


if __name__ == "__main__":
    unittest.main()
