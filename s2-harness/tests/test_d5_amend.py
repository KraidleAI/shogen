"""Lot D5-AMEND d'ADR-0028 (A-6 ; annexe D.5 amendée le 2026-09-30) : traitements descriptifs, hors
décision, sans paramètre : décomposition de K_s par lectures panne_transport et c_s
(SHOGEN-HOST-DEGRADED-1), τ observé par classe (SHOGEN-TAU-REDERIV-1), fenêtres sautées et bornes à P̂_more
fixé (SHOGEN-CENSURE-INFO-1), dans r1 puis au rendu (blocs 1 et 3, [SENSIBILITÉ]). Attendus écrits à la
main et scellés avant le code (journal G1 §4.2 ; FM-3.3) ; τ observé aussi contre un oracle d'une autre
forme (fractions ; population lue de r1.classify_cells et liée à ses hors-enveloppe) ; bornes rendues contre
des fractions. Lignes de journal construites ou collecteur réel, aucune donnée de campagne. Chaque test
nomme la mutation qui le rougit."""

from __future__ import annotations

import os
import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from unittest import mock

from shogen_s2 import collector, r1, records, window
from shogen_s2.model import Reading, Status
from shogen_s2.r1 import Ecart
from shogen_s2.sources import SIGMA_CLASS_OF_FLUX
from tests.test_collector import BY_ID, DELTA, FakeClock, _taumap, sbc_huge
from tests.test_r1 import mk, rd

POOL = list("abcdef")
SCOF = {**dict.fromkeys("abcd", "cA"), **dict.fromkeys("ef", "cB")}
SBC = {"cA": D(100), "cB": None}
PT = "panne_transport"
DK = {0: {"a": PT, "b": PT}, 1: {"a": PT, "b": None}, 2: {"a": "panne_http", "b": "panne_decode"},
      3: {"e": "200", "f": "200"}, 4: {"a": "100/200", "e": "200"}, 5: dict.fromkeys(POOL, PT),
      6: {"a": PT}, 7: dict.fromkeys(POOL), 8: dict.fromkeys("abc", PT), 9: {}}
TA = {**{j - 1: {"d": str(100 + j)} for j in range(1, 26)}, 25: {"d": "150/200"},
      26: {**dict.fromkeys("abc", "panne_http"), "d": "190"}}
TM = {0: {"c": "200", "d": "200", "e": None, "f": None}, 1: {"e": "50"}}
G = [int(datetime(2026, 8, 7, 23, 55, tzinfo=timezone.utc).timestamp()) + 60 * k for k in range(10)]
VEN = int(datetime(2026, 8, 7, 22, tzinfo=timezone.utc).timestamp())      # ven. 22:00Z : rang 0 (calme)
P6 = ["coinbase", "bitstamp", "gemini", "okx_index", "kraken", "binance"]
PAN = {0: {"coinbase": PT, "bitstamp": PT}, 1: {"kraken": PT, "binance": "http"},
       2: {"gemini": "http", "okx_index": "http"}, 3: dict.fromkeys(P6, PT),
       4: {"coinbase": PT, "kraken": "http"}, 5: {}}


def calcul(spec: dict, tau: str, stress=99, pool=POOL) -> tuple:
    """Fenêtre i : ws = 60·(i + 1), strate stress si i ≥ stress. Valeur par flux : None (lecture absente),
    statut de panne, ou « prix[/âge] » (ok ; source_ts = ws − âge pour cA, absent pour cB) ; défaut : ok
    à 100."""
    m, lec, t = [], [], {"cA": D(tau), "cB": D(tau)}
    for i, cas in spec.items():
        ws = 60 * (i + 1)
        m.append(mk(ws, "stress" if i >= stress else "calme"))
        for f in pool:
            v = cas.get(f, "100")
            if v is not None:
                p, _, age = v.partition("/")
                ok = not v.startswith("panne")
                lec.append(rd(ws, f, "ok" if ok else v, p if ok else None,
                              D(ws - int(age or 0)) if SCOF[f] == "cA" else None))
    return r1.compute_r1(m, lec, pool, 60, SBC, SCOF, t), m, lec, t


def oracle_tau(m, lec, t) -> tuple:
    """Fractions : cellules HORS_ENVELOPPE ou PAS_ECART de r1.classify_cells ; médiane des AUTRES
    répondantes de la fenêtre recalculée ici. Rend ({classe : ratios}, {classe : hors-enveloppe})."""
    px = {(r["window_start"], r["flux_id"]): F(r["price"]) for r in lec if r["status"] == "ok"}
    rat, he = {k: [] for k in t}, dict.fromkeys(t, 0)
    for (ws, f), e in r1.classify_cells(m, lec, POOL, 60, SBC, SCOF, t).items():
        if e in (Ecart.HORS_ENVELOPPE, Ecart.PAS_ECART):
            o = sorted(p for (x, g), p in px.items() if x == ws and g != f)
            med = (o[(len(o) - 1) // 2] + o[len(o) // 2]) / 2
            rat[SCOF[f]].append(abs(px[ws, f] - med) / med)
            he[SCOF[f]] += e is Ecart.HORS_ENVELOPPE
    return rat, he


def rang(k: int) -> int:
    return VEN + 60 * k


def lecture(spec, ts):
    """Fixture RF (§2.6) : statut par rang j mod 6 (PAN) ; okx_index à 100 + (j mod 5), 150 au rang 7 ;
    autres à 100 ; source_ts porté par les place_horodatee seules."""
    k, base = (int(ts) - VEN) // 60, dict(flux_id=spec.flux_id, kind=spec.kind, endpoint=spec.endpoint,
                                          fetch_ts=ts, currency=spec.currency)
    st = PAN[k % 6].get(spec.flux_id)
    if st:
        return Reading(status=Status.PANNE_TRANSPORT if st == PT else Status.PANNE_HTTP,
                       http_status=None if st == PT else 401, **base)
    okx = spec.flux_id == "okx_index"
    return Reading(status=Status.OK, http_status=200, price=D(150 if okx and k == 7 else 100 + k % 5 * okx),
                   source_ts=ts if SIGMA_CLASS_OF_FLUX[spec.flux_id] == "place_horodatee" else None, **base)


def rf() -> str:
    """Collecteur réel, w = 60, calendrier week-end, τ = 0,2 : rangs 0-239 puis 250-269 (trou 240-249,
    stress)."""
    d = tempfile.mkdtemp(prefix="s2d5_")
    paths = [os.path.join(d, x) for x in ("control.jsonl", "journal.jsonl", "raw.jsonl")]
    for a, b in ((0, 240), (250, 270)):
        clock = [float(rang(a))] + [t for k in range(a, b) for t in (rang(k) + 1.0, rang(k) + 60 - DELTA)]
        collector.collect([BY_ID[f] for f in P6], *paths, n_windows=b - a, sigma_by_class=sbc_huge(),
                          tau_classe=_taumap(D("0.2")), strate_spec=window.WEEKEND_STRATE_SPEC,
                          now_fn=FakeClock(clock), sleep_fn=lambda s: None, read_fn=lecture)
    return d


class TestDecompositionK(unittest.TestCase):
    def test_dk_composantes_somme_inclusions(self):
        """Fixture DK (fichier scellé §2.1). Rougit si : « ≥ 2 » écrit « > 2 » ; composante omise ou
        fusionnée (somme ≠ K) ; lecture absente comptée panne_transport (W1, W7) ; c_s sans « chaque flux
        du pool » ; tous_hors_enveloppe lu « au moins un hors-enveloppe » (W4) ; compteurs partagés entre
        strates."""
        out = calcul(DK, "0.3", stress=8)[0]
        att = {"calme": (7, 2, 1, 4, 1, 1), "stress": (1, 1, 0, 0, 0, 0)}
        for st, v in att.items():
            b = out["strates"][st]
            d = b["decomposition_K"]
            self.assertEqual((b["K"], d["pt_2_plus"], d["pt_1"], d["pt_0"], d["tous_hors_enveloppe"],
                              d["c"]), v)
            self.assertEqual(d["pt_2_plus"] + d["pt_1"] + d["pt_0"], b["K"])
            self.assertLessEqual(d["tous_hors_enveloppe"], d["pt_0"])
            self.assertLessEqual(d["c"], d["pt_2_plus"])

    def test_pool_vide_c_nul(self):
        """Pool vide, une fenêtre : c_s = 0. Rougit si : « chaque flux du pool » tenu sur un pool vide."""
        out = r1.compute_r1([mk(60)], [], [], 60, SBC, SCOF, {"cA": D("0.3")})
        self.assertEqual(out["strates"]["calme"]["decomposition_K"]["c"], 0)

    def test_pool_un_flux_c_hors_de_K(self):
        """Revue G2, C-1 (e) et C-2 : pool d'un flux, lecture panne_transport, un seul écart : K = 0 et
        c_s = 1 (c_s sur toutes les fenêtres de la strate, D-1). Rougit si : c_s limité à K (G12)."""
        b = calcul({0: {"a": PT}}, "0.3", pool=["a"])[0]["strates"]["calme"]
        self.assertEqual((b["K"], b["decomposition_K"]),
                         (0, dict(pt_2_plus=0, pt_1=0, pt_0=0, tous_hors_enveloppe=0, c=1)))

    def test_tous_hors_enveloppe_restreint_a_K(self):
        """Revue G2, C-1 (f), τ = 0,5 : fenêtre 0, f seul hors-enveloppe (un écart, hors de K) ; fenêtre 1,
        e et f hors-enveloppe (dans K). K = 1 = K[0] = K[tous les écarts hors_enveloppe]. Rougit si : cette
        composante comptée hors de K (G13)."""
        b = calcul({0: {"f": "200"}, 1: dict.fromkeys("ef", "200")}, "0.5")[0]["strates"]["calme"]
        self.assertEqual((b["K"], b["decomposition_K"]),
                         (1, dict(pt_2_plus=0, pt_1=0, pt_0=1, tous_hors_enveloppe=1, c=0)))


class TestTauObserve(unittest.TestCase):
    def controle(self, sortie, att):
        """att {classe : (N, P99, max)} écrits à la main ; puis égalité avec l'oracle en fractions et nombre
        de ratios > τ_classe = hors-enveloppe de classify_ecart."""
        out, m, lec, t = sortie
        rat, he = oracle_tau(m, lec, t)
        for cl, (n, p99, mx) in att.items():
            o, v = out["tau_observe"][cl], sorted(rat[cl])
            self.assertEqual((o["tau_classe"], o["N"], o["P99"], o["max"]),
                             (t[cl], n, p99 and D(p99), mx and D(mx)), cl)
            self.assertEqual(len(v), n)
            if v:
                self.assertEqual((F(o["P99"]), F(o["max"])), (v[(99 * n + 99) // 100 - 1], v[-1]))
            self.assertEqual(sum(x > F(t[cl]) for x in v), he[cl])

    def test_ta_rang_le_plus_proche_et_population(self):
        """Fixture TA (§2.2) : N = 103, P99 = 0,24 (rang 102), max = 0,25. Rougit si : P99 = max ; rang
        (99·N)//100 ; cellule périmée (W26) ou non évaluable (W27) dans la population ; classes confondues ;
        hors-enveloppe exclus."""
        self.controle(calcul(TA, "0.2"), {"cA": (103, "0.24", "0.25"), "cB": (52, "0", "0")})

    def test_dk_strates_cumulees_et_tm_mediane_loo(self):
        """DK : cumul sur les deux strates (cA 20, cB 14) ; TM (§2.3, addendum 2 §B.4) : médiane des AUTRES
        répondantes (0,5 et 1) ; écart sous la médiane (e = 50 : 0,5). Rougit si : τ observé de la dernière
        strate seulement ; médiane prise avec la cellule elle-même (1/3) ; valeur absolue retirée."""
        self.controle(calcul(DK, "0.3", stress=8), {"cA": (20, "0", "0"), "cB": (14, "1", "1")})
        self.controle(calcul(TM, "0.3"), {"cA": (8, "1", "1"), "cB": (2, "0.5", "0.5")})

    def test_contexte_decimal_ambiant_sans_effet(self):
        """Revue G2, C-1 (d), τ = 0,5 : f à 200 contre la médiane 150 des autres répondantes, rapport 1/3 ; τ
        observé de cB identique sous un contexte ambiant de précision 10 et 80 : 1/3 à 50 chiffres (précision
        fixée). Rougit si : précision non fixée dans _ecart_relatif (G06)."""
        spec, tiers = {0: {**dict.fromkeys("abcde", "150"), "f": "200"}}, D("0." + "3" * 50)
        for prec in (10, 80):
            with localcontext() as ctx:
                ctx.prec = prec
                o = calcul(spec, "0.5")[0]["tau_observe"]["cB"]
            self.assertEqual((o["N"], o["P99"], o["max"]), (2, tiers, tiers), prec)

    def test_rang_p99_n_multiple_de_100(self):
        """Revue G2, C-1 (g) : TA réduite aux fenêtres 0 à 24 et au pool abcd, N = 100 (75 rapports nuls,
        puis 0,01 à 0,25) ; P99 au rang 99 = 0,24 ; maximum 0,25. Rougit si : rang (99·N + 100)//100 (G14),
        décalé au seul bord entier (99·N multiple de 100), que TA (N = 103) ne voit pas."""
        self.controle(calcul({k: TA[k] for k in range(25)}, "0.2", pool=list("abcd")),
                      {"cA": (100, "0.24", "0.25")})


class TestCensure(unittest.TestCase):
    def test_bornes_valeurs_a_la_main(self):
        """§2.4. Rougit si : z_haut sans « + s » ; n au lieu de n + s ; bornes permutées ; variante σ̂_bloc
        sur l'erreur-type binomiale ; σ̂²_bloc absent lu comme une valeur."""
        b = r1.bornes_censure(96, 30, D("0.2"), 4, D(25))
        self.assertEqual([b[k] for k in ("s", "z_bas", "z_haut", "z_bloc_bas", "z_bloc_haut")],
                         [4, D("2.5"), D("3.5"), D(2), D("2.8")])
        b = r1.bornes_censure(96, 10, D("0.2"), 4)
        self.assertEqual([b[k] for k in ("z_bas", "z_haut", "z_bloc_bas", "z_bloc_haut")],
                         [D("-2.5"), D("-1.5"), None, None])

    def test_s_nul_egalite_exacte_z_et_z_bloc(self):
        """s = 0 : z_bas = z_haut = r1.z_score (même fonction que z_s) et = z_bloc de r1.bloc_strate (ℓ = 1,
        n = 100, K = 30 : σ̂² = 21), égalité Decimal exacte. Rougit si : autre forme de calcul (arrondi, ordre
        des opérations) ; imputation non nulle à s = 0."""
        b = r1.bloc_strate([(60 * i, int(i < 30)) for i in range(100)], 60, D("0.2"), D(16), ell=1)
        z = r1.bornes_censure(100, 30, D("0.2"), 0, b["sigma2_bloc"])
        self.assertEqual((b["sigma2_bloc"], z["z_bas"]), (D(21), D("2.5")))
        self.assertEqual((z["z_bas"], z["z_haut"]), (r1.z_score(100, 30, D("0.2")),) * 2)
        self.assertEqual((z["z_bloc_bas"], z["z_bloc_haut"]), (b["z_bloc"],) * 2)

    def test_fenetres_sautees_grille_portee_plages(self):
        """§2.5, addendum 2 §B.3 et §B.6. Rougit si : fenêtre exclue comptée sautée ; marqueur d'une plage
        retiré deux fois ; plages chevauchantes retirées deux fois ; fin de portée incluse ; t0 non aligné
        pris tel quel ; portée sans segment autre que [premier ; dernier + w) ; strate lue hors du
        calendrier ; marqueur hors grille ou calendrier non journalier accepté."""
        we, j, pl = window.WEEKEND_STRATE_SPEC, {G[0], G[2], G[3], G[6], G[7], G[9]}, [(G[7], G[8])]
        for borne, rg, att in ((None, pl, {"calme": 2, "stress": 1}), ((G[2], G[5]), pl, {"calme": 1}),
                               ((G[1] + 1, G[5]), pl, {"calme": 1}), (None, (), {"calme": 2, "stress": 2}),
                               (None, pl + [(G[8], G[8])], {"calme": 2, "stress": 1})):
            self.assertEqual(r1.fenetres_sautees(j, we, 60, borne, rg), att, borne)
        self.assertEqual(r1.fenetres_sautees(j, window.SINGLE_STRATE_SPEC, 60, None, pl), {"calme": 3})
        self.assertEqual(r1.fenetres_sautees(set(), we, 60), {})
        self.assertRaises(ValueError, r1.fenetres_sautees, {G[0] + 1}, we, 60)
        # kind que le calendrier accepterait (strate_from_spec substitué) : la garde de fenetres_sautees lève
        with mock.patch.object(r1, "strate_from_spec", lambda ws, spec: "x"):
            self.assertRaises(ValueError, r1.fenetres_sautees, j, {"kind": "horaire"}, 60)

    def test_fenetres_sautees_plages_desordre_bornes_fractionnaires(self):
        """Revue G2, C-1 (a) à (c) : mono-strate, w = 60, M_k = mer. 2026-08-05 10:00Z + 60·k, un seul jour
        UTC. (a) [M1 ; M8] et [M5 ; M6] dans le désordre, marqueurs M0 et M9 : rien ; (b) borne [M0 ; M3),
        plage [M5 ; M6] au-delà, le même jour : 2 ; (c) t0 = M1 + 0,5 exclut M1, t_fin = M3 + 0,5 inclut M3.
        Rougit si : fin d'union = b (G02) ; plages non triées avant l'union (G03) ; compte d'un jour non borné
        à 0 (G04) ; int au lieu de ceil sur les bornes (G05)."""
        m = [int(datetime(2026, 8, 5, 10, tzinfo=timezone.utc).timestamp()) + 60 * k for k in range(10)]
        for marq, borne, rg, att in (({m[0], m[9]}, None, [(m[5], m[6]), (m[1], m[8])], {}),
                                     ({m[0]}, (m[0], m[3]), [(m[5], m[6])], {"calme": 2}),
                                     ({m[0]}, (m[1] + 0.5, m[4]), (), {"calme": 2}),
                                     ({m[0]}, (m[1], m[3] + 0.5), (), {"calme": 3})):
            self.assertEqual(r1.fenetres_sautees(marq, window.SINGLE_STRATE_SPEC, 60, borne, rg), att, borne)

    def test_rf_recalcul_depuis_le_journal(self):
        """Fixture RF (§2.6, addendum 2 §B.1), collecteur réel : r1.recompute_from_journal, chemin du lecteur
        tiers, sert la décomposition de K et τ observé ; fenetres_sautees sur ses marqueurs. Rougit si : clé
        absente du recalcul depuis le journal ; composante de K, c_s ou τ observé faux ; trou de 10 fenêtres
        stress non compté."""
        d = rf()
        c, j = (os.path.join(d, x) for x in ("control.jsonl", "journal.jsonl"))
        out, k = r1.recompute_from_journal(c, j), ("pt_2_plus", "pt_1", "pt_0", "tous_hors_enveloppe", "c")
        for st, v in (("calme", (100, 40, 40, 20, 0, 20)), ("stress", (116, 46, 47, 23, 0, 23))):
            b = out["strates"][st]
            self.assertEqual((b["K"], *(b["decomposition_K"][x] for x in k)), v, st)
        tau = {cl: (o["N"], o["P99"], o["max"]) for cl, o in out["tau_observe"].items()}
        self.assertEqual((tau["place_horodatee"], tau["sans_horodatage"]),
                         ((652, D("0.04"), D("0.5")), (304, 0, 0)))
        ws = {m["window_start"] for m in records.parse_control(c)[2]}
        self.assertEqual(r1.fenetres_sautees(ws, window.WEEKEND_STRATE_SPEC, 60), {"stress": 10})


if __name__ == "__main__":
    unittest.main()
