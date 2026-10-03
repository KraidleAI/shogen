"""SHOGEN-TESTS-HOTE-DEUX-FLUX-1 (lot CORR, CORR-3 ; C-2 et C-3 de la relecture R-B) : un hôte à deux flux, comme
www.okx.com en production (okx_ticker, okx_index) : k nominal du segment en hôtes, k nominal_s en flux, aux entrées du
drapeau 2 et dans l'énoncé REJETTE ; branche « VRAI, borne supérieure de k_eff < k nominal → éteint ». Fixture :
collecteur réel, J1 de tests/test_critere.py (deux(25, 29) : coinbase et kraken en panne) sur quatre flux et trois
hôtes, ℓ = 1 par la couture de B-DEP-2 ; attendus écrits à la main. Mutants : journal G1 du lot CORR."""
from __future__ import annotations

import os
import tempfile
import unittest

from shogen_s2 import collector, r2, report, window
from shogen_s2.model import Reading, Status
from tests.test_collector import BY_ID, DELTA, TAU, FakeClock, _taumap, frozen_reading, sbc_huge
from tests.test_critere import bloc3, deux
from tests.test_rendu_blocs import SAM, couture

FLUX = ["coinbase", "kraken", "okx_ticker", "okx_index"]       # hôtes : coinbase, kraken, www.okx.com (deux flux)
T0 = SAM - 200 * 60                                             # 200 fenêtres calme, puis 200 stress


def journal4(asn) -> tuple:
    """J1 sur FLUX, w = 60 s ; relevés ASN de r2.collect_asn, asn(hôte) = (RIPEstat, Cymru)."""
    d = tempfile.mkdtemp(prefix="s2deux_")
    c, j, raw = (os.path.join(d, n) for n in ("control.jsonl", "journal.jsonl", "raw.jsonl"))

    def read_fn(s, ts):
        ws = int(ts) // 60 * 60
        if deux(25, 29)(s.flux_id, ws >= SAM, (ws - (SAM if ws >= SAM else T0)) // 60):
            return Reading(flux_id=s.flux_id, kind=s.kind, endpoint=s.endpoint, fetch_ts=ts, currency=s.currency,
                           status=Status.PANNE_HTTP, http_status=401)
        return frozen_reading(s.flux_id, ts)
    b, specs = range(T0, SAM + 200 * 60, 60), [BY_ID[f] for f in FLUX]
    collector.collect(specs, c, j, raw, n_windows=len(b), w=60, sigma_by_class=sbc_huge(), tau_classe=_taumap(TAU),
                      strate_spec=window.WEEKEND_STRATE_SPEC, sleep_fn=lambda s: None, read_fn=read_fn,
                      now_fn=FakeClock([float(b[0])] + [x for ws in b for x in (ws + 1.0, ws + 60 - DELTA)]))
    r2.collect_asn(specs, c, now_fn=lambda: float(SAM), resolve_fn=lambda h, rs: dict(
        zip(("asn_ripestat", "asn_cymru"), asn(h)), status="ok", resolver=rs[0], holder="TEST"))
    return c, j


class TestHoteDeuxFlux(unittest.TestCase):
    def test_leve_k_nominal_en_hotes_k_nominal_s_en_flux(self):
        """Un AS par hôte : k_eff = 3 = k nominal du segment (hôtes) → LEVÉ ; énoncé REJETTE avec k nominal_s = 4
        flux ; entrées du drapeau 2 : 4 flux par strate contre 3 hôtes, « comparaison hétérogène déclarée ». Rougit
        si : k nominal du drapeau 2 compté en flux (M03b de R-B) ; k nominal_s de l'énoncé compté en hôtes (M15) ;
        déclaration seulement si k nominal_s < k nominal (M06)."""
        a = {"api.exchange.coinbase.com": 64512, "api.kraken.com": 64513, "www.okx.com": 64514}
        c, j = journal4(lambda h: (a[h], a[h]))
        with couture(1):
            g = r2.recompute_r2_from_journal(c, j)["drapeau_2"]
            txt = report.render_report(c, j)
        self.assertEqual((g["etat"], g["k_eff"], g["k_nominal"], g["k_nominal_strates"]),
                         ("leve", 3, 3, {"calme": 4, "stress": 4}))
        self.assertIn("(k nominal_s = 4 flux du pool de la strate, bloc 1 ; k_eff mesuré = 3, bloc 6) est rejeté dans "
                      "la strate calme sur 200 fenêtres", bloc3(txt))
        self.assertIn(" ; k nominal du segment (hôtes) = 3 ; k nominal_s (flux du pool de la strate) : « calme » = 4, "
                      "« stress » = 4 — comparaison hétérogène déclarée ; strate poolée hors des entrées", txt)

    def test_eteint_borne_superieure_sous_k_nominal(self):
        """coinbase et kraken sur un même AS (fusion), www.okx.com discordant (non attribué) : k_eff ≤ 2 (borne
        supérieure) < k nominal = 3 → ÉTEINT (pt 10). Rougit si toute borne supérieure rend NON ÉVALUABLE (M01)."""
        c, j = journal4(lambda h: (64600, 65600) if h == "www.okx.com" else (64000, 64000))
        with couture(1):
            g = r2.recompute_r2_from_journal(c, j)["drapeau_2"]
        self.assertEqual((g["etat"], g["r1_discrimine"], g["k_eff"], g["k_nominal"]), ("eteint", "VRAI", 2, 3))
        self.assertEqual(g["raison"], "« R1 discrimine » VRAI (strate(s) : calme) mais k_eff ≤ 2 (borne supérieure) "
                         "< k nominal du segment = 3 : recouvrement R2 mesuré explique au moins en partie la "
                         "co-défaillance")


if __name__ == "__main__":
    unittest.main()
