"""Lot D5-AMEND d'ADR-0028 (A-6 ; annexe D.5 amendée le 2026-09-30) : traitements descriptifs, hors
décision, sans paramètre : décomposition de K_s par lectures panne_transport et c_s
(SHOGEN-HOST-DEGRADED-1), τ observé par classe (SHOGEN-TAU-REDERIV-1), fenêtres sautées et bornes à P̂_more
fixé (SHOGEN-CENSURE-INFO-1), dans r1 puis au rendu (blocs 1 et 3, [SENSIBILITÉ]). Attendus écrits à la
main et scellés avant le code (journal G1 §4.2 ; FM-3.3) ; τ observé aussi contre un oracle d'une autre
forme (fractions ; population lue de r1.classify_cells et liée à ses hors-enveloppe) ; bornes rendues contre
des fractions. Lignes de journal construites ou collecteur réel, aucune donnée de campagne. Chaque test
nomme la mutation qui le rougit."""

from __future__ import annotations

import unittest
from decimal import Decimal as D, localcontext
from fractions import Fraction as F

from shogen_s2 import r1
from shogen_s2.r1 import Ecart
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


if __name__ == "__main__":
    unittest.main()
