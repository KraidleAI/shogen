"""Lot CRITERE d'ADR-0028 (A-1, A-3, A-4) : règle SHOGEN-CRITERE-R1-1 (texte : ADR-0028 §1 bis.1, pts 1-11),
r1.regle_critere et sa section au bloc 3 de report.py. Attendus écrits à la main et scellés avant le code
(journal G1 du lot, §2 ; annexe C, FM-3.3) : table unitaire sur des strates au schéma de r1_out, puis
fixtures du collecteur réel (w = 60 s, la panne seule écart), valeurs en fractions ; ℓ ≠ 240 par la couture
de B-DEP-2 (D-10). Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import contextlib
import unittest
from decimal import Decimal as D
from fractions import Fraction as F

from shogen_s2 import r1
from tests.test_blocs import d50
from tests.test_collector import SKELETON as FL
from tests.test_rendu_blocs import couture, journal, proche

S1, NN, NEUF = "NON ÉVALUABLE", "NE REJETTE PAS", "2.32" + "9" * 49      # NEUF : 2,33 − 10⁻⁵¹


def blk(z, zb, garde="16", s2="9", n=1000) -> dict:
    """Strate au schéma de r1_out["strates"][s], clés lues par la règle seules (fichier scellé, §2.1)."""
    return {"z": None if z is None else D(z), "n": n, "gate_value": D(garde),
            "bloc": {"z_bloc": None if zb is None else D(zb), "sigma2_bloc": D(s2)}}


U = {"U1": (blk(None, "3", "5", "1", 100), S1, "garde_5_4", None),
     "U2": (blk("2.33", "3"), "REJETTE", "rejette", None),
     "U3": (blk("3", "2.33"), "REJETTE", "rejette", None),
     "U4": (blk(NEUF, "5"), NN, "z_sous_seuil", "12.6864"),
     "U5": (blk("3", NEUF, s2="25"), NN, "discordance", "15.8580"),
     "U6": (blk("3", None), S1, "rejet_non_qualifiable", None),
     "U7": (blk("-3", None), NN, "z_sous_seuil", "12.6864"),
     "U8": (blk("1", "5"), NN, "z_sous_seuil", "12.6864")}


def deux(oc: int, os_: int):
    """Fixtures J1, J2 : coinbase en panne aux rangs j < 50, kraken aux rangs o ≤ j < o + 50 (o = oc en calme,
    os_ en stress), bitstamp jamais ; K = max(0, 50 − o)."""
    def panne(f, st, j):
        o = os_ if st else oc
        return j < 50 if f == "coinbase" else f == "kraken" and o <= j < o + 50
    return panne


def rotation(f: str, st: bool, j: int) -> bool:
    """Fixture J3 : en calme, deux flux sur trois en panne à chaque fenêtre (FL[j mod 3] répond) ; rien en
    stress."""
    return not st and f != FL[j % 3]


def ell(n: int):
    """ℓ = 240 : chemin de production, sans couture ; sinon la couture r1.bloc_strate de B-DEP-2 (D-10)."""
    return contextlib.nullcontext() if n == 240 else couture(n)


def regle(c: str, j: str, n: int = 240) -> tuple:
    with ell(n):
        out = r1.recompute_from_journal(c, j)
    return out, r1.regle_critere(out)


class TestRegleTable(unittest.TestCase):
    def test_table_de_verite_par_strate(self):
        """U1 à U8. Rougit si : « ≥ » remplacé par « > » sur z_s (U2) ou sur z_bloc (U3) ; arrondi avant
        comparaison (U4, U5) ; z_bloc ignoré (U5, U6) ; z_s ignoré (U8) ; garde §5.4 ignorée (U1) ; EMD omis
        ou sur la seule erreur-type binomiale (U5)."""
        for nom, (b, v, cas, emd) in U.items():
            e = r1.regle_critere({"strates": {"a": b}})["strates"]["a"]
            self.assertEqual((e["valeur"], e["cas"]), (v, cas), nom)
            att = (None, None) if emd is None else (D(emd), D(emd) / 1000)
            self.assertEqual((e["emd"], e["emd_fraction"]), att, nom)

    def test_r1_discrimine_m_et_poolee(self):
        """C1 à C7. Rougit si : rejet non qualifiable sans effet sur FAUX (C3) ; m statique ; strate poolée
        parmi les entrées de la règle (C7) ; strates qui rejettent non nommées."""
        u = {k: v[0] for k, v in U.items()}
        for st, d, rej, tst, nq in (({"a": u["U2"], "b": u["U6"]}, "VRAI", ["a"], ["a"], ["b"]),
                                    ({"a": u["U4"], "b": u["U1"]}, "FAUX", [], ["a"], []),
                                    ({"a": u["U4"], "b": u["U6"]}, S1, [], ["a"], ["b"]),
                                    ({"a": u["U5"], "b": u["U8"]}, "FAUX", [], ["a", "b"], []),
                                    ({}, S1, [], [], []), ({"a": u["U1"], "b": u["U1"]}, S1, [], [], [])):
            g = r1.regle_critere({"strates": st})
            self.assertEqual((g["r1_discrimine"], g["rejette"], g["testees"], g["m"], g["non_qualifiables"]),
                             (d, rej, tst, len(tst), nq), list(st))
        g = r1.regle_critere({"strates": {"a": u["U4"]}, "poolee": {"z_pool": D(9), "variance": D(1)}})
        self.assertEqual((list(g["strates"]), g["r1_discrimine"], g["m"]), (["a"], "FAUX", 1))


class TestRegleFixtures(unittest.TestCase):
    """Fixtures journal J1 à J3 (fichier scellé §2.2) : collecteur réel → journal → compute_r1 → règle."""

    @classmethod
    def setUpClass(cls):
        cls.j1, cls.j2 = journal(200, 200, deux(25, 29)), journal(200, 200, deux(50, 37))
        cls.j3 = journal(54, 10, rotation)

    def test_j1_couture_l1_rejette_et_discordance(self):
        """ℓ = 1 : calme REJETTE (z² = 40/3, z_bloc² = 50/7) ; stress discordance (z² = 2312/375, z_bloc² =
        14450/3759, EMD² = 236324725119/1250000000) ; VRAI [calme], m = 2. Rougit si : z_bloc ignoré ;
        « > » à la place de « ≥ »."""
        out, g = regle(*self.j1, 1)
        for st, z2, zb2 in (("calme", F(40, 3), F(50, 7)), ("stress", F(2312, 375), F(14450, 3759))):
            b = out["strates"][st]
            self.assertTrue(proche(str(b["z"]), z2, True) and proche(str(b["bloc"]["z_bloc"]), zb2, True), st)
        self.assertEqual([(e["valeur"], e["cas"]) for e in g["strates"].values()],
                         [("REJETTE", "rejette"), (NN, "discordance")])
        self.assertTrue(proche(str(g["strates"]["stress"]["emd"]), F(236324725119, 1250000000), True))
        self.assertEqual((g["r1_discrimine"], g["rejette"], g["m"]), ("VRAI", ["calme"], 2))

    def test_j1_production_rejet_non_qualifiable(self):
        """ℓ = 240, sans couture : n = 200 < 7 200, z_bloc non publiée, z_s ≥ 2,33 dans les deux strates :
        rejet non qualifiable, NON ÉVALUABLE, m = 0. Rougit si : z_bloc ignoré ; non qualifiable lu FAUX."""
        _out, g = regle(*self.j1)
        self.assertEqual([e["cas"] for e in g["strates"].values()], ["rejet_non_qualifiable"] * 2)
        self.assertEqual((g["r1_discrimine"], g["m"], g["non_qualifiables"]), (S1, 0, ["calme", "stress"]))

    def test_j2_k0_negatif_et_emd_sigma_bloc(self):
        """ℓ = 240 : calme K = 0, z ≤ −2,33 (z² = 40/3), EMD² = 188607123/1600000 (garde) ; stress K = 13,
        z² = 8/375, σ̂²_bloc = 2064751/48000 > garde, z_bloc non publiée, EMD² = 43269638424597/10¹¹ (C-7) ;
        FAUX, m = 2. Rougit si : EMD sur la seule erreur-type binomiale ; K = 0 ou z négatif non testés."""
        out, g = regle(*self.j2)
        c, s = out["strates"]["calme"], out["strates"]["stress"]
        self.assertTrue(proche(str(c["z"]), F(40, 3), True) and c["z"] < 0)
        self.assertTrue(proche(str(s["z"]), F(8, 375), True))
        self.assertEqual(s["bloc"]["sigma2_bloc"], d50(2064751, 48000))
        for st, emd2 in (("calme", F(188607123, 1600000)), ("stress", F(43269638424597, 10 ** 11))):
            e = g["strates"][st]
            self.assertEqual((e["valeur"], e["cas"]), (NN, "z_sous_seuil"), st)
            self.assertTrue(proche(str(e["emd"]), emd2, True), st)
            self.assertTrue(proche(str(e["emd_fraction"]), emd2 / 40000, True), st)
        self.assertEqual((g["r1_discrimine"], g["m"]), ("FAUX", 2))

    def test_j3_k_egal_n_et_garde(self):
        """ℓ = 1 : calme K = n = 54, z² = 189/10, σ̂²_bloc = 0 (seul motif, garde de blocs tenue à ℓ = 1) :
        rejet non qualifiable ; stress P̂_more = 0 : garde §5.4 ; NON ÉVALUABLE, m = 0. Rougit si : z_bloc
        ignoré ; garde §5.4 ignorée."""
        out, g = regle(*self.j3, 1)
        c = out["strates"]["calme"]
        self.assertTrue(proche(str(c["z"]), F(189, 10), True) and c["K"] == c["n"] == 54)
        self.assertEqual(c["bloc"]["z_bloc_motif"], "σ̂²_bloc = 0 (K ∈ {0, n})")
        self.assertEqual([e["cas"] for e in g["strates"].values()], ["rejet_non_qualifiable", "garde_5_4"])
        self.assertEqual((g["r1_discrimine"], g["m"]), (S1, 0))


if __name__ == "__main__":
    unittest.main()
