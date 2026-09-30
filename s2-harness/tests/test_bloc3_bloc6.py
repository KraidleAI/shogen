"""Lot B d'ADR-0028, sous-lot B-b (D6 iv ; HS2-06, HS2-07) : bloc 3, définition d'écart et paramètres lus
de run_params ; bloc 6, date de la partition = ts du relevé asn_attribution retenu (dernier par hôte du pool,
après filtre de lecture), descriptif seulement (annexe D.5). Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from decimal import Decimal

from shogen_s2 import collector, r2, records, report, window
from tests.test_collector import BY_ID, DELTA, SKELETON, W, FakeClock, _taumap, frozen_read_fn, sbc_huge
from tests.test_exclusion import PLAGE, WS, build_fixture, poser

A = PLAGE[0]
DEF = ("  définition d'écart (10 §5.2 ; r1.classify_ecart), par fenêtre et par flux du pool d'analyse, "
       "précédence panne > staleness > hors-enveloppe : panne = lecture absente, statut ≠ ok ou prix "
       "absent ; staleness = win_end − source_ts > σ_classe de la classe du flux (σ_classe ou source_ts "
       "absent : non évaluée) ; hors-enveloppe = |p − médiane_LOO|/médiane_LOO > τ_classe, N ≥ n_min "
       "répondantes ; N < n_min, médiane_LOO ≤ 0 ou τ_classe absent : non évaluable (pas un écart) ; sinon "
       "pas d'écart ; K = fenêtres à ≥ 2 écarts — HS2-06")
DATE = "  date de la partition, axe ASN (ADR-0026 déc. 1 ; HS2-07) = "
DESCR = " — descriptif seulement (ADR-0028 annexe D.5)"


def bloc(txt: str, n: int) -> list:
    return txt.split(f"[BLOC {n}]")[1].split(f"[BLOC {n + 1}]")[0].splitlines()


class TestBloc3Bloc6(unittest.TestCase):
    def test_bloc3_definition_et_parametres_de_run_params(self):
        """HS2-06, C-8 : définition au bloc 3, sous l'en-tête ; σ_classe, τ_classe et n_min lus de run_params
        (τ = 0,0123, σ place_horodatee = 7777 s, n_min = 5 réécrit dans chaque run_params). Rougit si : τ,
        σ ou n_min codés en dur ; définition réécrite, absente ou hors du bloc 3."""
        d = tempfile.mkdtemp(prefix="s2b3_")
        c, j, raw = (os.path.join(d, n) for n in ("control.jsonl", "journal.jsonl", "raw.jsonl"))
        clock = [float(WS[0])] + [x for b in WS[:2] for x in (b + 1.0, b + W - DELTA)]
        collector.collect([BY_ID[f] for f in SKELETON], c, j, raw, n_windows=2,
                          sigma_by_class=dict(sbc_huge(), place_horodatee=Decimal("7777")),
                          tau_classe=_taumap(Decimal("0.0123")), strate_spec=window.WEEKEND_STRATE_SPEC,
                          now_fn=FakeClock(clock), sleep_fn=lambda s: None, read_fn=frozen_read_fn)
        with open(c, encoding="utf-8") as f:
            objs = [dict(o, n_min_hors_enveloppe=5) if o["record"] == "run_params" else o
                    for o in map(json.loads, f)]
        with open(c, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(o, ensure_ascii=False) + "\n" for o in objs)
        p = records.effective_run_params(records.parse_control(c)[0])
        self.assertEqual((p["sigma_classe"]["place_horodatee"], p["tau_classe"]["agregateur"]),
                         ("7777", "0.0123"))
        self.assertEqual(bloc(report.render_report(c, j), 3)[1:3], [DEF, (
            f"  paramètres (run_params, bloc 1) : σ_classe = {p['sigma_classe']} ; τ_classe = "
            f"{p['tau_classe']} ; n_min = 5")])

    def test_bloc6_date_releve_retenu_apres_filtre(self):
        """HS2-07, C-5 (iii), C-8 : sondes à A − 1 et A (poser), puis coinbase seul à A − 30 et un hôte hors
        pool à A − 50 : avec [PLAGE], min A − 30 et max A − 1 ; sans option, max A ; sans sonde : « non
        mesurée ». Rougit si : date lue avant filtre (tous[2]) ; premier relevé ou ts maximal au lieu du
        dernier retenu ; min et max inversés ; hôte hors pool compté ; « descriptif seulement » absent."""
        d = tempfile.mkdtemp(prefix="s2b6_")
        c, j = build_fixture(d)
        poser(d, (A - 1, A))
        ok = {"status": "ok", "asn_ripestat": 64600, "asn_cymru": 64600}
        r2.collect_asn([BY_ID["coinbase"]], c, resolve_fn=lambda h, r: ok, now_fn=lambda: float(A - 30))
        records.append_asn(c, records.asn_attribution_record("hors-pool.invalid", [], float(A - 50), [], ok))
        iso = report._iso_utc
        for rg, fin in (([PLAGE], A - 1), ((), A)):
            self.assertIn(f"{DATE}relevé asn_attribution retenu (dernier par hôte, après filtre de lecture) "
                          f": min {float(A - 30)} = {iso(A - 30)} ; max {float(fin)} = {iso(fin)} ; 3 / 3 "
                          f"hôtes du pool{DESCR}", bloc(report.render_report(c, j, exclude_ranges=rg), 6))
        sans = report.render_report(*build_fixture(tempfile.mkdtemp(prefix="s2b6n_")))
        self.assertIn(f"{DATE}non mesurée (aucun hôte du pool n'a de relevé asn_attribution retenu){DESCR}",
                      bloc(sans, 6))


if __name__ == "__main__":
    unittest.main()
