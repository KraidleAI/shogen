"""Tests de R2 (r2.py) — déterministes, sur entrées construites + fixtures mockées.

Familles exigées (mission M1c) et couverture :
  - ρ_raw ≈ 1 pour paire HONNÊTE, bas = signal (§4.2 (1)) ;
  - T = 1 sur copie EXACTE, T > T_Δ (§4.2 (2b)) ;
  - « historique de contenu insuffisant » sous N_min=300 (garde de conception, §4.2 ; SE de la transformation de Fisher : STAT 509 L7 §7.8) ;
  - k_eff = nombre de classes de la partition, clusters NOMMÉS (§5.6, ADR-0007) ;
  - drapeau 2 tri-état : levé (z≥2,33 + partition propre) / éteint / non évaluable (§5.6) ;
  - résolution ASN MOCKÉE (injection de dépendances) ;
  - fail-closed : ASN non mesuré → k_eff non évaluable ; discordance RIPEstat≠Cymru →
    pas de fusion ; clé porteuse R2 absente / strate trafiquée → recompute refusé (§E/§5.3).
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from decimal import Decimal

from shogen_s2 import collector, r2, records, report, window
from shogen_s2.model import Reading, Status
from shogen_s2.sources import SIGMA_CLASS_OF_FLUX, SPECS
from tests.test_collector import (
    BY_ID,
    CLOCK,
    SKELETON,
    FakeClock,
    frozen_read_fn,
    sbc_huge,
)
from tests.test_critere import blk
from tests.test_r1 import mk, rd
from tests.test_rendu_blocs import couture

D = Decimal
# [C2b] Étaient `SIGMA = D("1e12")` (σ SCALAIRE) et `TAU = D("50")` (τ ABSOLU).
# σ PAR CLASSE + τ RELATIF (ADR-0021). Ces tests bâtissent des co-défaillances par
# PANNE (prix identiques « 64000 » sinon) : σ/τ n'y produisent aucune staleness ni
# hors-enveloppe. `_sbc()` donne un plancher énorme à TOUTES les classes (aucune
# staleness, comme l'ancien 1e12) ; `_scof(pool)` mappe les flux réels par leur
# classe (sources) et les flux SYNTHÉTIQUES (a1,a2…) vers une classe de test énorme.
TAU = D("0.005")
PREC = r2.DECIMAL_PREC


def _taumap(t):
    """τ PAR CLASSE (ADR-0022) : diffuse un τ scalaire sur les 5 classes (adaptateur test)."""
    return {c: t for c in ("oracle_pyth", "oracle_chainlink", "agregateur",
                           "place_horodatee", "sans_horodatage")}


def _sbc() -> dict:
    """sigma_by_class « propre » : aucune staleness possible (planchers énormes),
    plus une classe de test `tclass` pour les flux synthétiques."""
    s = sbc_huge()
    s["tclass"] = D("1e12")
    return s


def _scof(pool) -> dict:
    """sigma_class_of_flux : flux réels par leur classe (source unique de vérité) ;
    flux synthétiques → `tclass` (plancher énorme → jamais stale, comme l'ancien σ)."""
    return {f: SIGMA_CLASS_OF_FLUX.get(f, "tclass") for f in pool}


def r2_params(flux_hosts=None, n_min=300):
    """run_params effectif minimal pour compute_r2 (clés R2 porteuses)."""
    return {
        "flux_hosts": flux_hosts or {}, "content_n_min": n_min,
        "content_kappa_value": 5, "content_jump_sigma": 4, "content_delta_windows": 1,
        "content_lag_l": 0, "content_big_l": 3, "tick_rule": "exact",
        "content_merge_criterion": r2.MERGE_CRITERION_V0,
    }


def asn_rec(host, asn_r=None, asn_c=None, holder="X", status="ok", ts=1.0):
    a = {"status": status}
    if status == "ok":
        a.update(ip="1.2.3.4", ip_secondary=[], cname_chain=[], prefix="p",
                 asn_ripestat=asn_r, asn_cymru=asn_c, holder=holder)
    return {"record": "asn_attribution", "host": host, "flux": [], "ts": ts,
            "resolvers": ["r"], **a}


def price_journal(n, price_fns, w=60, start=0):
    """Journal (markers, readings) de `n` fenêtres ; price_fns[flux](i) → Decimal|None."""
    markers, readings = [], []
    for i in range(n):
        ws = start + i * w
        markers.append(mk(ws))
        for f, fn in price_fns.items():
            p = fn(i)
            if p is None:
                readings.append(rd(ws, f, status="panne_http", price=None))
            else:
                readings.append(rd(ws, f, price=str(p), source_ts=D(ws)))
    return markers, readings


# ── Pearson ────────────────────────────────────────────────────────────────

class TestPearson(unittest.TestCase):
    def test_linear_is_plus_one(self):
        rho, _ = r2.pearson([D(1), D(2), D(3)], [D(2), D(4), D(6)])
        self.assertEqual(rho, D(1))

    def test_anti_is_minus_one(self):
        rho, _ = r2.pearson([D(1), D(2), D(3)], [D(3), D(2), D(1)])
        self.assertEqual(rho, D(-1))

    def test_constant_series_none(self):
        rho, note = r2.pearson([D(1), D(1), D(1)], [D(2), D(4), D(6)])
        self.assertIsNone(rho)
        self.assertIn("constante", note)

    def test_fixed_precision_deterministic(self):
        xs = [D(1) / D(3), D(2) / D(7), D(5) / D(11)]
        ys = [D(2), D(9), D(4)]
        self.assertEqual(r2.pearson(xs, ys)[0], r2.pearson(xs, ys)[0])


# ── Carte flux→hôte (agrégation flux→source réalisée) ────────────────────────

class TestFluxHost(unittest.TestCase):
    def test_okx_two_flux_one_host(self):
        fh = r2.build_flux_hosts(SPECS)
        self.assertEqual(fh["okx_ticker"], "www.okx.com")
        self.assertEqual(fh["okx_index"], "www.okx.com")

    def test_eleven_distinct_hosts(self):
        fh = r2.build_flux_hosts(SPECS)
        pool = [s.flux_id for s in SPECS]
        self.assertEqual(len(r2.hosts_of_pool(fh, pool)), 11)  # 12 flux, okx partagé
        self.assertEqual(r2.flux_by_host(fh, pool)["www.okx.com"],
                         ["okx_index", "okx_ticker"])


# ── Statistiques de contenu (§4.2) ───────────────────────────────────────────

class TestContentStats(unittest.TestCase):
    def _honest_and_signal(self, n=320):
        # A wiggle (période 7) ; B = A·1.0001 (rendements IDENTIQUES → ρ_raw≈1,
        # niveau différent → T=0) ; C = A exact (copie → T=1) ; D dynamique période 5.
        fns = {
            "A": lambda i: D(64000) + D((i % 7) * 10),
            "B": lambda i: (D(64000) + D((i % 7) * 10)) * D("1.0001"),
            "C": lambda i: D(64000) + D((i % 7) * 10),
            "Dd": lambda i: D(64000) + D((i % 5) * 13),
        }
        return price_journal(n, fns)

    def test_rho_raw_honest_near_one_and_low_is_signal(self):
        markers, readings = self._honest_and_signal()
        wins, rm = r2.price_map(readings, markers)
        lnp = r2.lnprice_by_window(wins, rm)
        honest = r2.rho_raw(wins, lnp, "A", "B", 60, 300)
        self.assertTrue(honest["sufficient"])
        self.assertGreater(honest["rho"], D("0.99"))          # plancher commun (≈1)
        signal = r2.rho_raw(wins, lnp, "A", "Dd", 60, 300)
        self.assertLess(abs(signal["rho"]), D("0.5"))         # bas = signal étrange

    def test_tick_identity_exact_copy_is_one_and_beats_shifted(self):
        markers, readings = self._honest_and_signal()
        wins, rm = r2.price_map(readings, markers)
        copy = r2.tick_identity(wins, rm, "A", "C", 60, 300, "exact", 1)
        self.assertEqual(copy["T"], D(1))                     # identité exacte
        self.assertTrue(copy["exact_copy_merge"])             # → fusion (§4.2 (2b))
        self.assertLess(copy["T_delta"], copy["T"])           # T ≫ T_Δ (contrôle décalé)
        # niveau différent (A vs B) → jamais fusion malgré ρ_raw≈1
        diff = r2.tick_identity(wins, rm, "A", "B", 60, 300, "exact", 1)
        self.assertEqual(diff["T"], D(0))
        self.assertFalse(diff["exact_copy_merge"])

    def test_constant_series_not_a_copy_merge(self):
        # peg gelé : deux séries CONSTANTES identiques → T=1 mais NON fusion (dégénéré).
        markers, readings = price_journal(320, {"P": lambda i: D(64000),
                                                 "Q": lambda i: D(64000)})
        wins, rm = r2.price_map(readings, markers)
        tk = r2.tick_identity(wins, rm, "P", "Q", 60, 300, "exact", 1)
        self.assertEqual(tk["T"], D(1))
        self.assertFalse(tk["non_constant"])
        self.assertFalse(tk["exact_copy_merge"])              # gelé ≠ copie (garde)

    def test_insufficient_history_below_n_min(self):
        markers, readings = self._honest_and_signal(n=50)
        wins, rm = r2.price_map(readings, markers)
        lnp = r2.lnprice_by_window(wins, rm)
        raw = r2.rho_raw(wins, lnp, "A", "B", 60, 300)
        self.assertIsNone(raw["rho"])
        self.assertFalse(raw["sufficient"])
        self.assertIn("historique de contenu insuffisant", raw["note"])

    def test_log_returns_skip_gaps(self):
        # une fenêtre absente (trou) → le rendement qui l'enjambe n'est PAS ponté.
        markers = [mk(0), mk(60), mk(180)]                    # trou : 120 absente
        readings = [rd(0, "A", price="100", source_ts=D(0)),
                    rd(60, "A", price="110", source_ts=D(60)),
                    rd(180, "A", price="120", source_ts=D(180))]
        wins, rm = r2.price_map(readings, markers)
        lnp = r2.lnprice_by_window(wins, rm)
        r = r2.log_returns(wins, lnp, "A", 60)
        self.assertIn(60, r)                                  # 0→60 adjacent : défini
        self.assertNotIn(180, r)                              # 60→180 non adjacent : exclu

    def test_rho_resid_requires_four_others(self):
        # ρ_resid exige ≥ 4 AUTRES répondantes/fenêtre (leave-two-out) ; pool de 3 flux
        # → 1 seul « autre » → aucune fenêtre évaluable → insuffisant (n=0).
        markers, readings = price_journal(320, {
            "A": lambda i: D(64000) + D(i % 7),
            "B": lambda i: D(64000) + D(i % 5),
            "Cc": lambda i: D(64000) + D(i % 3)})
        wins, rm = r2.price_map(readings, markers)
        lnp = r2.lnprice_by_window(wins, rm)
        res = r2.rho_resid(wins, lnp, "A", "B", 300, k_min=4)
        self.assertEqual(res["n"], 0)                         # < 4 autres → exclu
        self.assertFalse(res["sufficient"])


# ── Co-aberrance (2c) : réutilise la machinerie R1 §5.1 ──────────────────────

class TestCoaberrance(unittest.TestCase):
    def test_kz_counts_same_sign_and_reuses_r1_machinery(self):
        # `aber` construit à la main (indépendant du calcul de MAD) : A,B co-aberrants
        # de MÊME signe dans 20 fenêtres sur 60, indépendants ailleurs. K = 20.
        aber = {}
        for j in range(60):
            if j < 20:
                aber[j] = {"A": 1, "B": 1}                    # co-aberrants + (même signe)
            elif j < 30:
                aber[j] = {"A": 1, "B": -1}                   # signes opposés → pas compté
            else:
                aber[j] = {"A": 0, "B": 0}
        out = r2.coaberrance_kz(aber, "A", "B")
        self.assertEqual(out["n"], 60)
        self.assertEqual(out["K"], 20)                        # seules les MÊME-signe comptent
        # sous la garde §5.4 → queue exacte ; sinon z. La machinerie r1 est réutilisée.
        self.assertTrue(out["z"] is not None or out["queue"] is not None)

    def test_kz_degenerate_p_co_zero(self):
        # jamais de co-aberrance de même signe → p_co dépend des marginales ; ici A
        # toujours +, B toujours − → K=0, p_co=0 → dégénéré, pas de queue.
        aber = {j: {"A": 1, "B": -1} for j in range(15)}
        out = r2.coaberrance_kz(aber, "A", "B")
        self.assertEqual(out["K"], 0)
        self.assertIsNone(out["z"])
        self.assertIsNone(out["queue"])                       # dégénérée (§5.4)

    def test_aberrance_detects_clear_outlier(self):
        # pool étalé (MAD>0) + une source très au-dessus → aberrance + détectée.
        anchors = {"c1": 63000, "c2": 64000, "c3": 65000, "c4": 66000, "c5": 67000}
        fns = {f: (lambda i, v=v: D(v)) for f, v in anchors.items()}
        fns["A"] = lambda i: D(200000) if i == 5 else D(65000)   # outlier énorme à i=5
        markers, readings = price_journal(10, fns)
        wins, rm = r2.price_map(readings, markers)
        lnp = r2.lnprice_by_window(wins, rm)
        aber = r2._aberrance_by_window(wins, lnp, list(fns), D(5))
        self.assertEqual(aber[5 * 60]["A"], 1)                # aberrant + à i=5
        self.assertEqual(aber[0]["A"], 0)                     # dans l'enveloppe ailleurs


# ── δ direction (2d) ─────────────────────────────────────────────────────────

class TestDelta(unittest.TestCase):
    def test_direction_lead_lag(self):
        # Paliers PERMANENTS (un seul rendement par saut, pas de retour) et RARES :
        # σ reste petite → chaque saut dépasse 4σ. A saute à 30/60/90, B UNE fenêtre
        # après (31/61/91). B suit A → meilleur lag = +1 (« A précède B », §4.2 (2d)).
        def step(i, points):                                  # niveau = 64000 + 1000·(sauts passés)
            return D(64000) + D(1000 * sum(1 for p in points if i >= p))
        base = {f: (lambda i: D(64000)) for f in ("p1", "p2", "p3")}
        base["A"] = lambda i: step(i, (30, 60, 90))
        base["B"] = lambda i: step(i, (31, 61, 91))
        markers, readings = price_journal(120, base)
        wins, rm = r2.price_map(readings, markers)
        lnp = r2.lnprice_by_window(wins, rm)
        out = r2.delta_direction(wins, lnp, "A", "B", 60, D(4), 3)
        self.assertEqual(out["n_jumps_a"], 3)
        self.assertEqual(out["n_jumps_b"], 3)
        self.assertEqual(out["best_lag"], 1)                  # B suit A d'une fenêtre


# ── Partition ASN + k_eff + nommage (§5.6, ADR-0007) ─────────────────────────

class TestAsnPartition(unittest.TestCase):
    def _fh(self, hosts):
        return {f"f{i}": h for i, h in enumerate(hosts)}

    def test_cross_confirmed_shared_asn_merges(self):
        hosts = ["h0", "h1", "h2"]
        fh = self._fh(hosts)
        pool = list(fh)
        content = {"exact_copy_pairs": []}
        recs = [asn_rec("h0", 13335, 13335, "CLOUDFLARENET"),
                asn_rec("h1", 13335, 13335, "CLOUDFLARENET"),
                asn_rec("h2", 200, 200, "OTHER")]
        part = r2.compute_partition(recs, fh, pool, content)
        self.assertEqual(part["k_nominal"], 3)
        self.assertEqual(part["k_eff"], 2)                    # h0,h1 fusionnés
        names = [c["name"] for c in part["clusters"]]
        self.assertTrue(any("AS13335 CLOUDFLARENET" in n and "côté livraison" in n
                            for n in names))                  # NOMMÉ (ADR-0007)

    def test_discordant_ripestat_cymru_no_merge(self):
        hosts = ["h0", "h1"]
        fh = self._fh(hosts)
        recs = [asn_rec("h0", 13335, 13335), asn_rec("h1", 13335, 999)]  # h1 discordant
        part = r2.compute_partition(recs, fh, list(fh), {"exact_copy_pairs": []})
        self.assertEqual(part["asn_states"]["h1"]["kind"], "discordant")
        self.assertEqual(part["k_eff"], 2)                    # pas de fusion sur discordance

    def test_no_asn_records_keff_non_evaluable(self):
        fh = self._fh(["h0", "h1"])
        part = r2.compute_partition([], fh, list(fh), {"exact_copy_pairs": []})
        self.assertIsNone(part["k_eff"])                      # non évaluable, jamais fabriqué
        self.assertIn("NON MESURÉ", part["k_eff_note"])

    def test_incomplete_probing_keff_non_evaluable(self):
        fh = self._fh(["h0", "h1"])
        recs = [asn_rec("h0", 13335, 13335)]                  # h1 non sondé
        part = r2.compute_partition(recs, fh, list(fh), {"exact_copy_pairs": []})
        self.assertIsNone(part["k_eff"])
        self.assertIn("INCOMPLET", part["k_eff_note"])

    def test_failed_resolution_is_singleton_and_keff_upper_bound(self):
        fh = self._fh(["h0", "h1"])
        recs = [asn_rec("h0", 13335, 13335),
                asn_rec("h1", status="resolve_failed")]
        part = r2.compute_partition(recs, fh, list(fh), {"exact_copy_pairs": []})
        self.assertEqual(part["asn_states"]["h1"]["kind"], "resolve_failed")
        self.assertEqual(part["k_eff"], 2)                    # h1 singleton « non attribué »
        self.assertTrue(part["k_eff_is_upper_bound"])         # C-A : h1 gonfle k_eff
        self.assertEqual(part["n_unattributed"], 1)
        self.assertIn("h1", part["unattributed"])
        self.assertIn("BORNE SUPÉRIEURE", part["k_eff_note"])

    def test_all_attributed_keff_not_upper_bound(self):
        fh = self._fh(["h0", "h1"])
        recs = [asn_rec("h0", 13335, 13335), asn_rec("h1", 200, 200)]
        part = r2.compute_partition(recs, fh, list(fh), {"exact_copy_pairs": []})
        self.assertFalse(part["k_eff_is_upper_bound"])        # tous attribués → k_eff exact
        self.assertEqual(part["n_unattributed"], 0)

    def test_asn_divergence_published_not_overwritten(self):
        # deux relevés du même hôte à ASN différents (résidu 4) → divergence publiée.
        fh = self._fh(["h0", "h1"])
        recs = [asn_rec("h0", 13335, 13335, ts=1.0),
                asn_rec("h0", 16509, 16509, ts=2.0),          # re-mesure : ASN changé
                asn_rec("h1", 200, 200)]
        part = r2.compute_partition(recs, fh, list(fh), {"exact_copy_pairs": []})
        self.assertEqual(len(part["asn_divergences"]), 1)
        self.assertEqual(part["asn_divergences"][0]["host"], "h0")

    def test_echec_et_base_muette_ne_sont_pas_des_divergences(self):
        """SHOGEN-ASN-DIVERGENCE-ECHEC-1 (B-1 de R-B) : un relevé resolve_failed, ou à base muette, n'est ni une
        divergence ni la référence de la suivante ; un changement d'ASN vu à travers un échec en est une (relevé complet
        précédent) ; k_eff sur le dernier relevé par hôte, inchangé (h3 finit en échec : non attribué, borne
        supérieure). Rougit si : divergence tirée d'un relevé incomplet (sept à HEAD) ; changement perdu à travers un
        échec (comparaison au seul relevé précédent, M10 de R-B) ; k_eff lu sur le dernier relevé complet."""
        fh, ko = self._fh(["h0", "h1", "h2", "h3"]), "resolve_failed"
        recs = [asn_rec("h0", 1, 1, ts=1.0), asn_rec("h0", status=ko, ts=2.0), asn_rec("h0", 1, 1, ts=3.0),
                asn_rec("h1", 2, 2, ts=1.0), asn_rec("h1", 2, None, ts=2.0), asn_rec("h1", 2, 2, ts=3.0),
                asn_rec("h2", 3, 3, ts=1.0), asn_rec("h2", status=ko, ts=2.0), asn_rec("h2", 4, 4, ts=3.0),
                asn_rec("h3", 5, 5, ts=1.0), asn_rec("h3", status=ko, ts=2.0)]
        part = r2.compute_partition(recs, fh, list(fh), {"exact_copy_pairs": []})
        self.assertEqual(part["asn_divergences"], [{"host": "h2", "avant": (3, 3, 1.0), "apres": (4, 4, 3.0)}])
        self.assertEqual((part["k_eff"], part["k_eff_is_upper_bound"], part["unattributed"]), (4, True, ["h3"]))

    def test_rpc_read_path_caveat_carried(self):
        fh = {"chainlink": r2.RPC_READ_PATH_HOST}
        recs = [asn_rec(r2.RPC_READ_PATH_HOST, 10, 10)]
        part = r2.compute_partition(recs, fh, ["chainlink"], {"exact_copy_pairs": []})
        cav = part["clusters"][0]["caveats"]
        self.assertTrue(any("chemin de LECTURE" in c for c in cav))  # §3.2

    def test_content_exact_copy_merges_hosts(self):
        # deux hôtes DISTINCTS par ASN, mais flux copies exactes → fusion CONTENU.
        fh = {"A": "hostA", "C": "hostC"}
        recs = [asn_rec("hostA", 10, 10), asn_rec("hostC", 20, 20)]
        content = {"exact_copy_pairs": [frozenset(("A", "C"))]}
        part = r2.compute_partition(recs, fh, ["A", "C"], content)
        self.assertEqual(part["k_eff"], 1)                    # fusionnés par copie contenu
        self.assertTrue(any(m["axis"] == "content_exact_copy"
                            for m in part["merge_reasons"]))
        # C-B : label selon l'axe RÉEL — copie cross-ASN ≠ « côté livraison ».
        cl = part["clusters"][0]
        self.assertIn("content_exact_copy", cl["merge_axes"])
        self.assertIn("COPIE DE CONTENU", cl["name"])
        self.assertNotIn("côté livraison", cl["name"])        # jamais pour une copie
        self.assertNotIn("asn_measured", cl["merge_axes"])    # ASN 10≠20 → pas de fusion ASN

    def test_shared_asn_cluster_labeled_cote_livraison(self):
        # symétrique de C-B : fusion ASN partagé → « côté livraison » (fronting, résidu 1).
        fh = {"A": "hostA", "C": "hostC"}
        recs = [asn_rec("hostA", 13335, 13335, "CF"), asn_rec("hostC", 13335, 13335, "CF")]
        part = r2.compute_partition(recs, fh, ["A", "C"], {"exact_copy_pairs": []})
        cl = part["clusters"][0]
        self.assertIn("asn_measured", cl["merge_axes"])
        self.assertIn("côté livraison", cl["name"])
        self.assertNotIn("COPIE DE CONTENU", cl["name"])


# ── Drapeau 2 (§5.6) — tri-état ──────────────────────────────────────────────

class TestDrapeau2(unittest.TestCase):
    def _cofailure(self, n_windows, n_cofail, flux=("binance", "coinbase")):
        markers, readings = [], []
        for i in range(n_windows):
            ws = i * 60
            markers.append(mk(ws))
            for f in flux:
                if i < n_cofail:
                    readings.append(rd(ws, f, status="panne_http", price=None))
                else:
                    readings.append(rd(ws, f, price="64000", source_ts=D(ws + 1)))
        return markers, readings

    def test_leve_when_z_signif_and_clean_partition(self):
        # binance & coinbase : hôtes DISTINCTS, ASN distincts → k_eff = k nominal. Lot CRITERE : la règle
        # exige z_bloc publiée ; couture ℓ = 1 (n = 60 ≥ 30) : z² = 20, z_bloc² = 15, « R1 discrimine » VRAI.
        fh = r2.build_flux_hosts(SPECS)
        markers, readings = self._cofailure(60, 30)
        recs = [asn_rec("api.binance.com", 10, 10),
                asn_rec("api.exchange.coinbase.com", 20, 20)]
        with couture(1):
            out = r2.compute_r2(markers, readings, recs, ["binance", "coinbase"], 60,
                                _sbc(), _scof(["binance", "coinbase"]), _taumap(TAU), r2_params(fh))
        self.assertEqual(out["drapeau_2"]["etat"], "leve")
        d2 = out["drapeau_2"]
        self.assertEqual((d2["r1_discrimine"], d2["rejette"]), ("VRAI", ["calme"]))
        self.assertIsNotNone(out["drapeau_2"]["localisation_inter_clusters"])

    def test_eteint_when_shared_asn(self):
        fh = r2.build_flux_hosts(SPECS)
        markers, readings = self._cofailure(60, 30)
        recs = [asn_rec("api.binance.com", 13335, 13335, "CF"),
                asn_rec("api.exchange.coinbase.com", 13335, 13335, "CF")]
        with couture(1):                                         # lot CRITERE : « R1 discrimine » VRAI
            out = r2.compute_r2(markers, readings, recs, ["binance", "coinbase"], 60,
                                _sbc(), _scof(["binance", "coinbase"]), _taumap(TAU), r2_params(fh))
        self.assertEqual(out["partition"]["k_eff"], 1)
        self.assertEqual(out["drapeau_2"]["etat"], "eteint")

    def test_non_evaluable_when_no_z(self):
        fh = r2.build_flux_hosts(SPECS)
        markers, readings = self._cofailure(3, 2)             # court → pas de z
        recs = [asn_rec("api.binance.com", 10, 10),
                asn_rec("api.exchange.coinbase.com", 20, 20)]
        out = r2.compute_r2(markers, readings, recs, ["binance", "coinbase"], 60,
                            _sbc(), _scof(["binance", "coinbase"]), _taumap(TAU), r2_params(fh))
        self.assertEqual(out["drapeau_2"]["etat"], "non_evaluable")

    def test_eteint_when_z_below_threshold(self):
        # unité : z publié mais < 2,33 → NE REJETTE PAS, « R1 discrimine » FAUX → éteint (lot CRITERE).
        r1_out = {"strates": {"calme": {**blk("1.5", None), "per_source": {}}}}
        part = {"k_eff": 2, "k_nominal": 2, "clusters": []}
        lm_out = {"strates": {}}
        d2 = r2.drapeau_2(r1_out, part, lm_out)
        self.assertEqual(d2["etat"], "eteint")

    def test_non_evaluable_when_keff_none(self):
        r1_out = {"strates": {"calme": {**blk("5", "5"), "per_source": {}}}}          # REJETTE : VRAI
        part = {"k_eff": None, "k_nominal": 3, "clusters": []}
        d2 = r2.drapeau_2(r1_out, part, {"strates": {}})
        self.assertEqual(d2["etat"], "non_evaluable")


# ── Arêtes méthode (§4.3) — basis:doc déclenche (b), ne fusionne pas ─────────

class TestMethodEdges(unittest.TestCase):
    def test_five_basis_doc_edges(self):
        self.assertEqual(len(r2.METHOD_EDGES), 5)
        for e in r2.METHOD_EDGES:
            self.assertEqual(e["basis"], "doc")
            self.assertIn("doc_url", e)
            self.assertIn("doc_fetched", e)

    def test_upstream_edges_trigger_content_not_merge(self):
        # coingecko←binance, pyth←coinbase, defillama←coingecko : déclenchent (b).
        trig = r2.method_edge_pairs()
        self.assertIn(frozenset(("binance", "coingecko")), trig)
        self.assertIn(frozenset(("coinbase", "pyth")), trig)
        self.assertIn(frozenset(("coingecko", "defillama")), trig)
        # mais NE fusionnent PAS : hôtes distincts, ASN distincts → k_eff intact.
        fh = r2.build_flux_hosts(SPECS)
        pool = ["binance", "coingecko"]
        recs = [asn_rec("api.binance.com", 10, 10),
                asn_rec("api.coingecko.com", 20, 20)]
        part = r2.compute_partition(recs, fh, pool, {"exact_copy_pairs": []})
        self.assertEqual(part["k_eff"], 2)                    # basis:doc n'a pas fusionné


# ── Corrélations entre clusters (§5.5 pt 4) ──────────────────────────────────

class TestClusterCorrelations(unittest.TestCase):
    def test_cluster_correlation_for_multi_member(self):
        # Deux clusters de 2 FLUX chacun (okx-like : 2 flux/hôte) → cluster à ≥2 membres.
        # hA = {a1,a2} ; hB = {b1,b2} ; ASN distincts (pas de fusion inter-cluster).
        fh = {"a1": "hA", "a2": "hA", "b1": "hB", "b2": "hB"}
        recs = [asn_rec("hA", 100, 100, "ASA"), asn_rec("hB", 200, 200, "ASB")]
        pool = ["a1", "a2", "b1", "b2"]
        markers, readings = [], []
        for i in range(10):
            ws = i * 60
            markers.append(mk(ws))
            # cluster A co-fails on even i ; cluster B on odd i (anti-correlated Θ̂)
            for f in ("a1", "a2"):
                readings.append(rd(ws, f, status="panne_http", price=None) if i % 2 == 0
                                else rd(ws, f, price="64000", source_ts=D(ws)))
            for f in ("b1", "b2"):
                readings.append(rd(ws, f, status="panne_http", price=None) if i % 2 == 1
                                else rd(ws, f, price="64000", source_ts=D(ws)))
        content = {"exact_copy_pairs": []}
        part = r2.compute_partition(recs, fh, pool, content)
        cc = r2.cluster_lm_correlations(part, markers, readings, pool, 60,
                                        _sbc(), _scof(pool), TAU, 4)
        self.assertEqual(cc["n_multi_clusters"], 2)
        self.assertEqual(len(cc["cluster_pairs"]), 1)
        v = next(iter(cc["cluster_pairs"].values()))
        self.assertEqual(v["signe"], "−")                     # Θ̂ anti-corrélés (Cov<0 publié)


# ── collect_asn : injection de dépendances (résolveur mockable) ──────────────

class TestCollectAsn(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2asn_")
        self.control = os.path.join(self.d, "control.jsonl")

    def test_mock_resolver_writes_records_read_by_parse_asn(self):
        specs = [BY_ID[f] for f in SKELETON]
        calls = []

        def mock(host, resolvers):
            calls.append(host)
            return {"status": "ok", "resolver": resolvers[0], "ip": "1.2.3.4",
                    "ip_secondary": [], "cname_chain": [], "prefix": "p",
                    "asn_ripestat": 13335, "asn_cymru": 13335, "holder": "CF"}

        recs = r2.collect_asn(specs, self.control, resolve_fn=mock,
                              now_fn=lambda: 1.0, pool=SKELETON)
        self.assertEqual(len(recs), 3)                        # 3 hôtes distincts
        self.assertEqual(sorted(calls), sorted({BY_ID[f].endpoint.split("/")[2]
                                                for f in SKELETON}))
        # parse_asn les relit ; parse_control les IGNORE (rétro-compat).
        self.assertEqual(len(records.parse_asn(self.control)), 3)
        _pl, _cc, mks = records.parse_control(self.control)
        self.assertEqual(mks, [])                             # aucun window_close ici

    def test_real_resolver_is_the_default_seam(self):
        # DI : le défaut EST le résolveur réel (non lancé ici) — le seam existe et
        # les tests l'ont remplacé par un mock (jamais de réseau en test).
        import inspect
        sig = inspect.signature(r2.collect_asn)
        self.assertIs(sig.parameters["resolve_fn"].default, r2.resolve_host_real)


# ── recompute_r2_from_journal : patron maison (fail-closed, déterminisme) ─────

class TestRecomputeHousePattern(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="s2r2rec_")
        self.control = os.path.join(self.d, "control.jsonl")
        self.journal = os.path.join(self.d, "journal.jsonl")
        self.raw = os.path.join(self.d, "raw.jsonl")
        specs = [BY_ID[f] for f in SKELETON]
        collector.collect(specs, self.control, self.journal, self.raw, n_windows=3,
                          sigma_by_class=_sbc(), tau_classe=_taumap(TAU), now_fn=FakeClock(CLOCK),
                          sleep_fn=lambda s: None, read_fn=frozen_read_fn)

        def mock(host, resolvers):
            m = {"api.exchange.coinbase.com": 13335, "api.kraken.com": 13335,
                 "www.bitstamp.net": 200}
            return {"status": "ok", "resolver": resolvers[0], "ip": "1.2.3.4",
                    "ip_secondary": [], "cname_chain": [], "prefix": "p",
                    "asn_ripestat": m[host], "asn_cymru": m[host], "holder": "H"}

        r2.collect_asn(specs, self.control, resolve_fn=mock, now_fn=lambda: 1.0,
                       pool=SKELETON)

    def test_recompute_keff_and_partition(self):
        out = r2.recompute_r2_from_journal(self.control, self.journal)
        self.assertEqual(out["partition"]["k_nominal"], 3)
        self.assertEqual(out["partition"]["k_eff"], 2)        # coinbase+kraken (AS13335)

    def test_report_asn_table_dated_and_r3_stated(self):
        # §6 bloc 5 : la table ASN porte la DATE (« résolveur, heure ») ; bloc 6 DIT
        # que R3 ne modifie jamais k_eff. ts=1.0 (setUp) → 1970-01-01 UTC déterministe.
        txt = report.render_report(self.control, self.journal)
        self.assertIn("heure(UTC)", txt)                      # colonne heure (mission/§6)
        self.assertIn("1970-01-01T00:00:01+00:00", txt)       # date datée, déterministe
        self.assertIn("R3", txt)
        self.assertIn("ne modifie JAMAIS k_eff", txt)         # §5.6 / 04 §3
        self.assertIn("k_eff     = 2", txt)                   # partition mesurée rendue

    def test_deterministic(self):
        a = r2.recompute_r2_from_journal(self.control, self.journal)
        b = r2.recompute_r2_from_journal(self.control, self.journal)
        self.assertEqual(a["partition"]["k_eff"], b["partition"]["k_eff"])
        self.assertEqual(report.render_report(self.control, self.journal),
                         report.render_report(self.control, self.journal))

    def test_report_marks_keff_upper_bound_on_unattributed(self):
        # C-A : un hôte resolve_failed → le rendu porte « BORNE SUPÉRIEURE » + le compte.
        d = tempfile.mkdtemp(prefix="s2ub_")
        control = os.path.join(d, "control.jsonl")
        j = os.path.join(d, "journal.jsonl")
        raw = os.path.join(d, "raw.jsonl")
        specs = [BY_ID[f] for f in SKELETON]
        collector.collect(specs, control, j, raw, n_windows=3, sigma_by_class=_sbc(),
                          tau_classe=_taumap(TAU), now_fn=FakeClock(CLOCK), sleep_fn=lambda s: None,
                          read_fn=frozen_read_fn)

        def mock(host, resolvers):
            if host == "www.bitstamp.net":                   # résolution échouée
                return {"status": "resolve_failed", "resolver": resolvers[0], "note": "SERVFAIL"}
            return {"status": "ok", "resolver": resolvers[0], "ip": "1.2.3.4",
                    "ip_secondary": [], "cname_chain": [], "prefix": "p",
                    "asn_ripestat": 13335, "asn_cymru": 13335, "holder": "CF"}

        r2.collect_asn(specs, control, resolve_fn=mock, now_fn=lambda: 1.0, pool=SKELETON)
        out = r2.recompute_r2_from_journal(control, j)
        self.assertTrue(out["partition"]["k_eff_is_upper_bound"])
        self.assertEqual(out["partition"]["n_unattributed"], 1)
        txt = report.render_report(control, j)
        self.assertIn("k_eff     ≤", txt)                     # marqueur de tête
        self.assertIn("BORNE SUPÉRIEURE", txt)
        self.assertIn("hôte(s) non attribué(s)", txt)

    def test_peg_path_end_to_end(self):
        # C3 : vraie paire USD×USDT + historique ≥ N_min → peg_pairs non vide + bloc 1
        # residu_peg count>0. binance = USDT ; 5 autres USD ; ≥4 « autres » pour ρ_resid.
        d = tempfile.mkdtemp(prefix="s2peg_")
        control = os.path.join(d, "control.jsonl")
        j = os.path.join(d, "journal.jsonl")
        raw = os.path.join(d, "raw.jsonl")
        pool_ids = ["binance", "coinbase", "kraken", "bitstamp", "gemini", "okx_index"]
        specs = [BY_ID[f] for f in pool_ids]
        n, start = 305, 1785000000
        clock = [float(start)]
        for i in range(n):
            clock += [float(start + i * 60 + 1), float(start + i * 60 + 55)]
        offs = {f: k for k, f in enumerate(pool_ids)}

        def read_fn(spec, ts):
            i = (int(ts) - start) // 60
            price = Decimal(64000) + Decimal((i % 11) * 5) + Decimal(offs[spec.flux_id])
            return Reading(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                           fetch_ts=ts, status=Status.OK, http_status=200, raw=b"x",
                           price=price, currency=spec.currency, source_ts=ts)

        collector.collect(specs, control, j, raw, n_windows=n, sigma_by_class=_sbc(),
                          tau_classe=_taumap(Decimal("1e9")), now_fn=FakeClock(clock),
                          sleep_fn=lambda s: None, read_fn=read_fn)
        out = r2.recompute_r2_from_journal(control, j)
        peg = out["content"]["peg_pairs"]
        self.assertGreater(len(peg), 0)                       # peg_pairs non vide (≥ N_min)
        self.assertTrue(all("binance" in k for k in peg))     # binance(USDT) × un USD
        txt = report.render_report(control, j)
        self.assertNotIn("paires USDT×USD : 0", txt)          # bloc 1 count > 0
        self.assertIn("residu_peg_usdt_usd", txt)

    def test_missing_r2_load_bearing_key_fail_closed(self):
        # clé R2 porteuse retirée → recompute R2 refusé (§E) ; R1 reste recalculable.
        with open(self.control, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for i, ln in enumerate(lines):
            obj = json.loads(ln)
            if obj.get("record") == "run_params":
                obj.pop("flux_hosts", None)                   # clé de partition retirée
                lines[i] = json.dumps(obj, ensure_ascii=False)
                break
        with open(self.control, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        with self.assertRaises(ValueError):
            r2.recompute_r2_from_journal(self.control, self.journal)
        with self.assertRaises(ValueError):
            report.render_report(self.control, self.journal)
        # R1 (jeu de clés découplé) reste recalculable sans la clé R2.
        from shogen_s2 import r1
        self.assertEqual(r1.recompute_from_journal(self.control, self.journal)
                         ["strates"]["calme"]["n"], 3)

    def test_tampered_strate_fail_closed(self):
        # strate trafiquée → les TROIS points d'entrée recalculables refusent (§5.3).
        specs = [BY_ID[f] for f in SKELETON]
        d = tempfile.mkdtemp(prefix="s2r2str_")
        control = os.path.join(d, "control.jsonl")
        j = os.path.join(d, "journal.jsonl")
        raw = os.path.join(d, "raw.jsonl")
        collector.collect(specs, control, j, raw, n_windows=3, sigma_by_class=_sbc(),
                          tau_classe=_taumap(TAU), strate_spec=window.WEEKEND_STRATE_SPEC,
                          now_fn=FakeClock([float(1785000000 + 60 * i) for i in range(7)]),
                          sleep_fn=lambda s: None, read_fn=frozen_read_fn)
        with open(control, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for i, ln in enumerate(lines):
            obj = json.loads(ln)
            if obj.get("record") == "window_close":
                obj["strate"] = "calme" if obj["strate"] == "stress" else "stress"
                lines[i] = json.dumps(obj, ensure_ascii=False)
                break
        with open(control, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        with self.assertRaises(ValueError):
            r2.recompute_r2_from_journal(control, j)


if __name__ == "__main__":
    unittest.main()
