"""Lot B-DEP-1 d'ADR-0028 (A-1, A-2 ; §1 bis.1 pts 3 et 9) : variance de long terme par blocs de la
série I_t = 1{m_t ≥ 2} d'une strate (Künsch 1989, P-01, OCR seul, [2nd] : blocs mobiles, noyau de
Bartlett, forme non restreinte), à comptes entiers par lag sur la grille UTC. Oracles écrits sous
d'autres formes que le code : énumération explicite des paires (Fraction) ; sommes de blocs de la série
centrée complétée par des 0 (entiers, CRITIQUE v2 §4.1) ; valeurs à la main recopiées de la commande
(88/75, 208/75). Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import json
import random
import tempfile
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction
from unittest import mock

from shogen_s2 import r1
from tests.test_sensibilite import H, fixture      # module de tests du lot B (couplage déclaré au G1)

W = 60
S1 = (0, 1, 1, 0, 0, 0, 1, 0, 0, 1)                # CRITIQUE v2 §4.1, recopiées de la commande
S2 = (1, 1, 0, 0, 0, 0, 0, 1, 1, 0)


def serie(bits, w=W, t0=0, pos=None) -> list:
    """Couples (window_start, I_t) aux positions `pos` (défaut 0..n−1) de la grille de pas w depuis t0."""
    return [(t0 + w * p, i) for p, i in zip(range(len(bits)) if pos is None else pos, bits)]


def blocs_numerateur(s, w, ell) -> int:
    """Oracle : N = Σ_j (Σ_{t ∈ bloc j} (n·I_t − K))², blocs de longueur ℓ sur la grille complétée
    par des 0 (identité de la CRITIQUE v2 §4.1) ; N = ℓ·n²·σ̂²."""
    n, k = len(s), sum(i for _, i in s)
    y = {(x - s[0][0]) // w: n * i - k for x, i in s}
    return sum(sum(y.get(t, 0) for t in range(j, j + ell)) ** 2 for j in range(1 - ell, max(y) + 1))


def enum_sigma2(s, w, ell) -> Fraction:
    """Oracle : toutes les paires (a, b), a avant b, d'écart k·w avec k < ℓ, énumérées une à une."""
    n, k = len(s), sum(i for _, i in s)
    y = [Fraction(n * i - k, n) for _, i in s]
    tot = sum(v * v for v in y)
    for a in range(n):
        for b in range(a + 1, n):
            lag = (s[b][0] - s[a][0]) // w
            if lag < ell:
                tot += 2 * (1 - Fraction(lag, ell)) * y[a] * y[b]
    return tot


def demi_ulp(d: Decimal, exact: Fraction) -> bool:
    """Vrai si d est à au plus une demi-unité de son 50e chiffre significatif de la valeur exacte."""
    return abs(Fraction(d) - exact) <= Fraction(10) ** (d.adjusted() - r1.DECIMAL_PREC + 1) / 2


def d50(num, den) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = r1.DECIMAL_PREC
        return Decimal(num) / Decimal(den)


class TestVarianceBlocsPure(unittest.TestCase):
    def test_valeurs_a_la_main_n10_l3(self):
        """n = 10, ℓ = 3 : σ̂² = 88/75 et 208/75, N = 352 et 832, γ̂₀ = 12/5 (CRITIQUE v2
        §4.1) ; Decimal égaux (== et str) à la division correctement arrondie à la précision 50.
        Rougit si : poids 1 − k/ℓ omis ; centrage omis ; γ̂₀ non centré ; lag ℓ inclus ; poids
        du lag 0 doublé ; S_g + S_d remplacé ; précision par défaut."""
        for bits, num, a in ((S1, 352, 88), (S2, 832, 208)):
            v = r1.block_long_run_variance(serie(bits), W, 3)
            self.assertEqual((v["n"], v["K"], v["numerateur"]), (10, 4, num))
            for x, y in ((v["sigma2_bloc"], d50(a, 75)), (v["gamma0"], Decimal("2.4"))):
                self.assertEqual((x, str(x)), (y, str(y)))

    def test_identite_l1_gamma0(self):
        """ℓ = 1 : σ̂²_bloc = γ̂₀ = n·Ī(1 − Ī) = K(n − K)/n, avec ou sans trous (CRITIQUE
        v2 §4.1). Rougit si : γ̂₀ non centré ; poids du lag 0 doublé."""
        for bits, pos in ((S1, None), ((1, 0, 1, 1, 0), (0, 3, 4, 9, 11)), ((1, 1, 1), None),
                          ((0, 1, 1), None)):
            v = r1.block_long_run_variance(serie(bits, pos=pos), W, 1)
            exact = Fraction(sum(bits) * (len(bits) - sum(bits)), len(bits))
            self.assertEqual(v["sigma2_bloc"], v["gamma0"])
            self.assertTrue(demi_ulp(v["gamma0"], exact), (bits, v))

    def test_serie_a_runs_facteur_calcule(self):
        """Série à runs I = (1,1,1,1,0,0,0,0), ℓ = 4 (valeur à la main du journal G1, §4) :
        γ̂₀ = 2, σ̂² = 17/4, σ̂²/γ̂₀ = 17/8 > 1 ; sommes de blocs : N = 4·8²·17/4 = 1 088.
        Rougit si : poids 1 − k/ℓ omis ; centrage omis."""
        s = serie((1, 1, 1, 1, 0, 0, 0, 0))
        v = r1.block_long_run_variance(s, W, 4)
        self.assertEqual((v["numerateur"], v["gamma0"], v["sigma2_bloc"]),
                         (1088, Decimal(2), Decimal("4.25")))
        self.assertEqual(Fraction(v["sigma2_bloc"]) / Fraction(v["gamma0"]), Fraction(17, 8))
        self.assertEqual(blocs_numerateur(s, W, 4), 1088)

    def test_positivite_trous_sommes_de_blocs(self):
        """Grilles trouées tirées (graine fixe), ℓ ∈ {1, 2, 3, 5, 8}, w ∈ {60, 3600}, origine
        quelconque : N égale l'oracle des sommes de blocs (entier) ; σ̂² ≥ 0, à une demi-unité du
        50e chiffre de N/(ℓ·n²) ; σ̂² = 0 ⇔ K ∈ {0, n}. Rougit si : paire hors grille (rang au
        lieu de position) ; M_k sans trous (n − k) ; poids ou centrage omis."""
        rnd = random.Random(20260930)
        for cas in range(120):
            w, ell = rnd.choice((60, 3600)), rnd.choice((1, 2, 3, 5, 8))
            p, pos = rnd.choice((0.0, 0.3, 0.7, 1.0)), sorted(rnd.sample(range(40), rnd.randint(1, 25)))
            s = serie([int(rnd.random() < p) for _ in pos], w, t0=rnd.randint(0, 10 ** 6), pos=pos)
            v, n, k = r1.block_long_run_variance(s, w, ell), len(s), sum(i for _, i in s)
            self.assertEqual(v["numerateur"], blocs_numerateur(s, w, ell), (cas, s, ell))
            self.assertTrue(demi_ulp(v["sigma2_bloc"], Fraction(v["numerateur"], ell * n * n)))
            self.assertGreaterEqual(v["sigma2_bloc"], 0)
            self.assertEqual(v["sigma2_bloc"] == 0, k in (0, n), (cas, s, ell))

    def test_bit_identite_deux_appels(self):
        """Deux appels sur une série trouée : sorties égales, Decimal de même str (ADR-0003) ; ℓ par
        défaut = 240. Rougit si : sortie non déterministe ou non Decimal ; ELL_BLOC ≠ 240."""
        s = serie((1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1), pos=(0, 1, 2, 4, 5, 6, 9, 10, 11, 13, 14))
        a, b = r1.block_long_run_variance(s, W), r1.block_long_run_variance(tuple(s), W)
        self.assertEqual((a, a), (b, r1.block_long_run_variance(s, W, 240)))
        for c in ("gamma0", "sigma2_bloc"):
            self.assertIs(type(a[c]), Decimal)
            self.assertEqual(str(a[c]), str(b[c]))

    def test_contrat_entree(self):
        """Contrat d'entrée (C-2) : écart w/2 ou 1,5·w, window_start dupliqué ou décroissant,
        I_t = 2, window_start non entier, w = 0, ℓ = 0 : ValueError ; série vide : n = 0, sorties
        à None. Rougit si : écart non multiple de w accepté ; doublon accepté."""
        for s, w, ell in (([(0, 1), (30, 0)], 60, 3), ([(0, 1), (90, 0)], 60, 3),
                          ([(0, 1), (0, 0)], 60, 3), ([(120, 1), (60, 0)], 60, 3), ([(0, 2)], 60, 3),
                          ([(0.0, 1)], 60, 3), ([(0, 1)], 0, 3), ([(0, 1)], 60, 0),
                          ([(0, 1), ("60", 0)], 60, 3), ([(0, 1), (None, 0)], 60, 3)):  # G2 C-4
            with self.assertRaises(ValueError, msg=(s, w, ell)):
                r1.block_long_run_variance(s, w, ell)
        self.assertEqual(r1.block_long_run_variance([], W),
                         {"n": 0, "K": 0, "numerateur": None, "gamma0": None, "sigma2_bloc": None})


SCHEMA = {"ell", "gamma0", "sigma2_bloc", "cv_theorique", "FIV", "R_centrage", "FIV_serie", "FIV_motif",
          "FIV_serie_motif", "z_bloc", "z_bloc_motif", "runs"}
P3, VIDE = Decimal("0.3"), "aucune fenêtre (n = 0)"


def bloc(bits, p=P3, ell=3, pos=None, w=W) -> dict:
    s = serie(bits, w, pos=pos)
    return r1.bloc_strate(s, w, p, r1.gate_value(len(s), p), ell)


class TestBlocStrate(unittest.TestCase):
    def test_schema_ferme_valeurs_a_la_main(self):
        """S1 (n = 10, ℓ = 3), P̂_more = 0,3 (garde 2,1) : 12 clés ; γ̂₀ = 12/5, R_centrage = 8/7 (==
        et str) ; FIV et FIV_serie à une demi-unité de σ̂²/garde et σ̂²/γ̂₀ (valeurs publiées), à
        1E-48 de 176/315 et 22/45 ; FIV = R_centrage × FIV_serie sur les Fraction exactes (C-4).
        Rougit si : FIV divisé par γ̂₀ ; R_centrage inversé."""
        b = bloc(S1)
        self.assertEqual((set(b), set(b["runs"])), (SCHEMA, {"nombre", "longueur_moyenne", "run_max"}))
        g, s2, g0 = Fraction(r1.gate_value(10, P3)), Fraction(b["sigma2_bloc"]), Fraction(b["gamma0"])
        self.assertEqual((b["ell"], g, g0), (3, Fraction(21, 10), Fraction(12, 5)))
        self.assertEqual((b["R_centrage"], str(b["R_centrage"])), (d50(8, 7), str(d50(8, 7))))
        for cle, exact in (("FIV", s2 / g), ("R_centrage", g0 / g), ("FIV_serie", s2 / g0)):
            self.assertTrue(demi_ulp(b[cle], exact), cle)
        self.assertEqual(s2 / g, (g0 / g) * (s2 / g0))
        for cle, cible in (("FIV", Fraction(176, 315)), ("FIV_serie", Fraction(22, 45))):
            self.assertLess(abs(Fraction(b[cle]) - cible), Fraction(1, 10 ** 48), cle)
        self.assertEqual((b["FIV_motif"], b["FIV_serie_motif"]), (None, None))

    def test_cv_theorique_racines_exactes(self):
        """cv_theorique = √(4ℓ/(3n)) : ℓ = 3, n = 100 → 0,2 ; ℓ = 3, n = 4 → 1. Rougit si : cv en
        √(3ℓ/(4n))."""
        self.assertEqual(bloc([1, 0] * 50)["cv_theorique"], Decimal("0.2"))
        self.assertEqual(bloc([1, 0, 0, 1])["cv_theorique"], Decimal(1))

    def test_garde_de_blocs_frontiere_et_garde_5_4(self):
        """Garde de blocs n ≥ 30·ℓ : ℓ = 3, n = 90 publie z_bloc, 89 non (motif chiffré) ; ℓ = 1, 30
        publie, 29 non. P̂_more = 0,1 : garde §5.4 = 8,1 < 10 à n = 90, z_bloc publié quand même
        (pt 3) ; z_bloc² = (K − n·P̂)²/σ̂² à 1E-45 près en relatif. Rougit si : garde ignorée ; « ≥ »
        en « > » ; z_bloc soumis à la garde §5.4 ; dénominateur binomial."""
        p = Decimal("0.1")
        self.assertLess(r1.gate_value(90, p), r1.SEUIL_HIST)
        for ell, n in ((3, 90), (1, 30)):
            for m in (n, n - 1):
                bits = [int(t % 5 == 0) for t in range(m)]
                b = bloc(bits, p, ell)
                if m < n:
                    self.assertIsNone(b["z_bloc"])
                    self.assertEqual(b["z_bloc_motif"], f"garde de blocs : n_s = {m} < 30·ℓ = {n}")
                    continue
                num = sum(bits) - m * Fraction(p)
                self.assertIsNone(b["z_bloc_motif"])
                self.assertGreater(b["z_bloc"], 0)
                ecart = Fraction(b["z_bloc"]) ** 2 * Fraction(b["sigma2_bloc"]) / (num * num) - 1
                self.assertLess(abs(ecart), Fraction(1, 10 ** 45))

    def test_sigma2_nul_motifs(self):
        """K ∈ {0, n}, n = 30 ≥ 30·ℓ (ℓ = 1) : σ̂² = 0, z_bloc absent, seul motif « σ̂²_bloc = 0
        (K ∈ {0, n}) » ; FIV_serie absent (γ̂₀ = 0), FIV = 0 ; n = 5 : les deux motifs joints.
        Rougit si : σ̂² = 0 non gardé (division par zéro)."""
        for bits in ([0] * 30, [1] * 30):
            b = bloc(bits, Decimal("0.1"), 1)
            self.assertEqual((b["sigma2_bloc"], b["z_bloc"], b["FIV"], b["FIV_serie"]), (0, None, 0, None))
            self.assertEqual((b["z_bloc_motif"], b["FIV_serie_motif"]),
                             ("σ̂²_bloc = 0 (K ∈ {0, n})", "γ̂₀ = 0 (K ∈ {0, n}) : FIV_serie indéfini"))
        self.assertEqual(bloc([0] * 5, Decimal("0.1"), 1)["z_bloc_motif"],
                         "σ̂²_bloc = 0 (K ∈ {0, n}) ; garde de blocs : n_s = 5 < 30·ℓ = 30")

    def test_degeneres_n0_garde_nulle(self):
        """P̂_more = 0 (garde 0) : FIV et R_centrage absents, FIV_motif ; série vide : 12 clés, valeurs
        à None, motif « aucune fenêtre (n = 0) », runs (0, None, 0). Rougit si : FIV non gardé."""
        b = bloc([0, 0, 0], Decimal(0))
        self.assertEqual((b["FIV"], b["R_centrage"], b["FIV_motif"]),
                         (None, None, "garde n·P̂_more·(1 − P̂_more) ≤ 0 : FIV, R_centrage indéfinis"))
        self.assertEqual(r1.bloc_strate([], W, P3, Decimal(0), 3), {
            "ell": 3, "gamma0": None, "sigma2_bloc": None, "cv_theorique": None, "FIV": None,
            "R_centrage": None, "FIV_serie": None, "FIV_motif": VIDE, "FIV_serie_motif": VIDE,
            "z_bloc": None, "z_bloc_motif": VIDE,
            "runs": {"nombre": 0, "longueur_moyenne": None, "run_max": 0}})

    def test_runs_grille(self):
        """Runs sur la grille : positions (0, 1, 2, 4, 5, 7), I = (1, 1, 1, 1, 1, 0) : le trou en 3
        coupe, deux runs (3 et 2), longueur moyenne 5/2 ; (1, 0, 1) contigu : deux runs de 1. Rougit
        si : run non coupé par un trou ; longueur moyenne = K/n."""
        r = bloc((1, 1, 1, 1, 1, 0), pos=(0, 1, 2, 4, 5, 7))["runs"]
        self.assertEqual(r, {"nombre": 2, "longueur_moyenne": Decimal("2.5"), "run_max": 3})
        self.assertEqual(bloc((1, 0, 1))["runs"], {"nombre": 2, "longueur_moyenne": Decimal(1), "run_max": 1})

    def test_trous_de_grille_enumeration_explicite(self):
        """Séries trouées tirées (graine fixe ; ℓ ∈ {2, 3, 7, 240} ; w ∈ {60, 3600} ; positions < 300) :
        σ̂²_bloc à une demi-unité du 50e chiffre de l'énumération explicite des paires ; une paire
        d'écart ≥ ℓ·w ne compte pas. Rougit si : paire hors grille ; M_k sans trous ; lag ℓ inclus."""
        rnd = random.Random(930)
        for cas in range(60):
            w, ell = rnd.choice((60, 3600)), rnd.choice((2, 3, 7, 240))
            pos = sorted(rnd.sample(range(300), rnd.randint(2, 30)))
            s = serie([int(rnd.random() < 0.4) for _ in pos], w, t0=7 * w, pos=pos)
            b = r1.bloc_strate(s, w, P3, r1.gate_value(len(s), P3), ell)
            self.assertTrue(demi_ulp(b["sigma2_bloc"], enum_sigma2(s, w, ell)), (cas, s, ell))

    def test_serie_iterateur(self):
        """G2 C-3 (D-15) : un itérateur donne la même clé `bloc` qu'une liste (deux parcours : variance,
        runs). Rougit si : bloc_strate parcourt deux fois l'objet de l'appelant."""
        s = serie((1, 1, 1, 1, 1, 0), pos=(0, 1, 2, 4, 5, 7))
        g = r1.gate_value(len(s), P3)
        self.assertEqual(r1.bloc_strate(iter(s), W, P3, g, 3), r1.bloc_strate(s, W, P3, g, 3))


class TestBlocIntegration(unittest.TestCase):
    def test_integration_fixture_recompute(self):
        """C-7 : fixture du lot B (`tests.test_sensibilite.fixture` : w = 3600 s, blocs séparés par des
        trous, reprise en doublons, calme et stress contigus) par `recompute_from_journal` : (i) 12 clés
        par strate ; (ii) Σ I_t = K_s ; (iii) z_bloc absent, motif « garde de blocs » (n_s < 7 200) ;
        (iv) fenêtres de la série = celles de la strate relues du control.jsonl ; σ̂² = énumération
        explicite (ℓ = 240) ; série augmentée des fenêtres des autres strates à I = 0 : σ̂² différent.
        Rougit si : clé absente ; sommande ≠ celle de K ; garde ignorée ; paire entre strates ; ℓ de
        compute_r1 ≠ ELL_BLOC ; ELL_BLOC ≠ 240 ou GARDE_BLOCS ≠ 30."""
        self.assertEqual((r1.ELL_BLOC, r1.GARDE_BLOCS), (240, 30))
        c, j = fixture(tempfile.mkdtemp(prefix="s2bdep1_"))
        with mock.patch.object(r1, "bloc_strate", wraps=r1.bloc_strate) as espion:
            out = r1.recompute_from_journal(c, j)
        with open(c, encoding="utf-8") as f:
            strate_de = {o["window_start"]: o["strate"] for o in map(json.loads, f)
                         if o.get("record") == "window_close"}
        self.assertEqual((sorted(out["strates"]), espion.call_count), (["calme", "stress"], 2))
        for appel in espion.call_args_list:
            s, w = appel.args[0], appel.args[1]
            st = strate_de[s[0][0]]
            blk, ell = out["strates"][st], r1.ELL_BLOC
            self.assertEqual((len(appel.args), appel.kwargs), (4, {}))         # G2 C-1 : ℓ par défaut
            self.assertEqual(appel.args[1:], (H, blk["P_more"], blk["gate_value"]))   # w, P̂_more, garde
            b, g = blk["bloc"], blk["gate_value"]
            self.assertEqual((b["FIV"], b["R_centrage"], b["FIV_serie"]),
                             (d50(b["sigma2_bloc"], g), d50(b["gamma0"], g),
                              d50(b["sigma2_bloc"], b["gamma0"])))
            self.assertEqual([x for x, _ in s], sorted(x for x in strate_de if strate_de[x] == st))
            self.assertEqual((len(s), sum(i for _, i in s)), (blk["n"], blk["K"]))
            self.assertEqual((set(blk["bloc"]), blk["bloc"]["z_bloc"]), (SCHEMA, None))
            self.assertEqual(blk["bloc"]["z_bloc_motif"], f"garde de blocs : n_s = {len(s)} < 30·ℓ = 7200")
            self.assertTrue(demi_ulp(blk["bloc"]["sigma2_bloc"], enum_sigma2(s, w, ell)))
            autres = sorted(s + [(x, 0) for x in strate_de if strate_de[x] != st])
            self.assertNotEqual(enum_sigma2(autres, w, ell), enum_sigma2(s, w, ell))

    def test_z_bloc_publie_par_compute_r1(self):
        """G2 C-2 : z_bloc publié par compute_r1 (n = 30·ℓ = 7 200, une strate, deux flux, co-pannes par
        runs) : même numérateur K − n·P̂_more que z_s (P̂_more de la strate), FIV = σ̂²/garde ; n = 7 199 :
        motif de garde de blocs. Rougit si : P̂_more ou garde d'une autre source passés à bloc_strate."""
        from tests.test_r1 import R1, SIGMA_HUGE, mk, rd
        for n in (7200, 7199):
            ws = [1786147200 + 60 * t for t in range(n)]
            down = [2 if (t // 40) % 9 == 0 else (1 if t % 3 == 0 else 0) for t in range(n)]
            rds = [rd(x, f, status="panne_http" if j < m else "ok") for x, m in zip(ws, down)
                   for j, f in enumerate("ab")]
            blk = R1([mk(x) for x in ws], rds, ["a", "b"], sigma=SIGMA_HUGE)["strates"]["calme"]
            b = blk["bloc"]
            if n < 7200:
                self.assertEqual((b["z_bloc"], b["z_bloc_motif"]),
                                 (None, "garde de blocs : n_s = 7199 < 30·ℓ = 7200"))
                continue
            num = blk["K"] - n * Fraction(blk["P_more"])
            self.assertIsNone(b["z_bloc_motif"])
            for z, var in ((b["z_bloc"], b["sigma2_bloc"]), (blk["z"], blk["gate_value"])):
                ecart = Fraction(z) ** 2 * Fraction(var) / (num * num) - 1
                self.assertLess(abs(ecart), Fraction(1, 10 ** 45))
                self.assertGreater(Fraction(z) * num, 0)
            self.assertEqual(b["FIV"], d50(b["sigma2_bloc"], blk["gate_value"]))


if __name__ == "__main__":
    unittest.main()
