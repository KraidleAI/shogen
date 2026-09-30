"""Lot POOLEE d'ADR-0028 (D2 pt 4 ; §1 bis.1 pt 9) : strate poolée en forme stratifiée,
z_pool = Σ_s (K_s − n_s·P̂_s) / √(Σ_s n_s·P̂_s·(1 − P̂_s)), sous r1_out["poolee"], jamais dans
r1_out["strates"]. Valeurs écrites à la main avant le code (journal G1 du lot, §4). Fixtures du collecteur
réel à w = 60 s : ven. 2026-08-07 21:04Z → sam. 00:00Z, 176 fenêtres calme, puis 64 stress ; j = rang de
la fenêtre dans sa strate. Chaque test nomme la mutation qui le rougit."""

from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timezone
from decimal import Decimal, localcontext

from shogen_s2 import r1, records
from tests.test_exclusion import WS, build_fixture
from tests.test_sensibilite import fixture

T0 = int(datetime(2026, 8, 7, 21, 4, tzinfo=timezone.utc).timestamp())
SAM = T0 + 176 * 60                                  # sam. 2026-08-08 00:00Z : première fenêtre stress
E = Decimal("1e-40")                                 # écart admis aux valeurs irrationnelles (prec 50)
DEG = " (dégénérée : P̂_more ∈ {0,1})"
GARDE = "strate(s) sous la garde §5.4, z de strate non publié : "


def journal(nominale: bool) -> tuple:
    """Simpson : coinbase et kraken en plan produit dans chaque strate (K_s = n_s·P̂_s) ; nominale : en
    calme, kraken tombe avec coinbase (K = 44). bitstamp jamais en panne ; la panne est le seul écart
    (σ énorme, N = 3 < 4 répondantes)."""
    def en_panne(f, ws):
        st, j = ws >= SAM, (ws - (SAM if ws >= SAM else T0)) // 60
        if f == "coinbase":
            return j < (56 if st else 44)
        return f == "kraken" and (j % 8 != 7 if st else (j < 44 if nominale else j % 4 == 0))
    return fixture(tempfile.mkdtemp(prefix="s2poolee_"), blocs=[range(T0, SAM + 64 * 60, 60)], w=60,
                   en_panne=en_panne)


def a_sur_racine(a: int, b: int) -> Decimal:
    """a/√b à la précision 60 : forme réduite de la valeur écrite à la main (journal G1, §4)."""
    with localcontext() as ctx:
        ctx.prec = 60
        return Decimal(a) / Decimal(b).sqrt()


def blk(n, k, p, z, queue=True) -> dict:
    return {"n": n, "K": k, "P_more": Decimal(p), "z": z, "queue_exacte_applicable": queue,
            "per_source": {"a": {}, "b": {}}}


class TestPooleeR1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.simpson, cls.nominale = journal(False), journal(True)

    def test_formule_valeurs_a_la_main_identite_denominateur_nul(self):
        """[(100, 30, 1/4), (50, 5, 1/10)] : 5, 23,25, 10/√93. Rougit si : dénominateur non stratifié
        (5/√24) ; P̂ d'un terme pour tous ; numérateur non centré ; un terme ≠ z_score ; garde du
        dénominateur nul retirée."""
        num, var, z = r1.z_pool_stratifie([(100, 30, Decimal("0.25")), (50, 5, Decimal("0.1"))])
        self.assertEqual((num, var), (5, Decimal("23.25")))
        self.assertLess(abs(z - a_sur_racine(10, 93)), E)
        p = Decimal("0.0625")
        self.assertEqual(r1.z_pool_stratifie([(176, 44, p)])[2], r1.z_score(176, 44, p))
        with self.assertRaises(ValueError):
            r1.z_pool_stratifie([(10, 0, Decimal(0)), (5, 5, Decimal(1))])

    def test_simpson_union_gonflee_stratifiee_nulle(self):
        """K_s = n_s·P̂_s, P̂ = 1/16 (calme) et 49/64 (stress) : z_s = 0, z_pool = 0 ; l'union brute des
        240 fenêtres donne 2640/√714000 = 3,12… ≥ 2,33. Rougit si : z_pool sur l'union ; P̂ d'une strate
        pour toutes."""
        c, j = self.simpson
        out = r1.recompute_from_journal(c, j)
        self.assertEqual({st: (b["n"], b["K"], b["P_more"], b["z"]) for st, b in out["strates"].items()},
                         {"calme": (176, 11, Decimal("0.0625"), 0),
                          "stress": (64, 49, Decimal("0.765625"), 0)})
        po = out["poolee"]
        self.assertEqual((po["numerateur"], po["variance"], po["z_pool"], po["motif"]),
                         (0, Decimal("21.796875"), 0, None))
        plist, _clock, m = records.parse_control(c)
        p = records.effective_run_params(plist)
        u = r1.compute_r1([dict(x, strate="union") for x in m], r1.parse_journal(j), list(p["pool"]), 60,
                          *records.sigma_tau_from_params(p))["strates"]["union"]
        self.assertEqual((u["n"], u["K"]), (240, 60))
        self.assertLess(abs(u["z"] - a_sur_racine(2640, 714000)), E)
        self.assertGreaterEqual(u["z"], r1.SEUIL_Z)

    def test_nominale_valeur_a_la_main_et_entrees(self):
        """Calme : numérateur 33 ; z_pool = 33/√21,796875 = 264/√1395 = 7,068… ; entrées n, K, P̂ et pool
        D1 par strate. Rougit si : dénominateur non stratifié (33/√45) ; P̂ d'une strate pour toutes ;
        entrées absentes."""
        out = r1.recompute_from_journal(*self.nominale)
        po = out["poolee"]
        self.assertEqual((po["numerateur"], po["variance"], po["motif"]), (33, Decimal("21.796875"), None))
        self.assertLess(abs(po["z_pool"] - a_sur_racine(264, 1395)), E)
        self.assertLess(abs(out["strates"]["calme"]["z"] - a_sur_racine(132, 165)), E)   # 33/√10,3125
        pool = ["coinbase", "kraken", "bitstamp"]
        self.assertEqual(po["strates"], {
            "calme": {"n": 176, "K": 44, "P_more": Decimal("0.0625"), "pool": pool, "N": 3},
            "stress": {"n": 64, "K": 49, "P_more": Decimal("0.765625"), "pool": pool, "N": 3}})

    def test_poolee_jamais_dans_strates_cle_separee(self):
        """ADR-0028 §1 bis.1 pt 9 : r1_out["strates"] = strates du calendrier seules ; poolée sous
        r1_out["poolee"], aussi au retour « aucune fenêtre ». Rougit si : poolée insérée dans
        r1_out["strates"] (donc dans z_max et les entrées de r2.drapeau_2) ; clé absente du retour
        précoce ; étiquette réécrite."""
        out = r1.recompute_from_journal(*self.simpson)
        self.assertEqual((sorted(out["strates"]), out["poolee"]["etiquette"]),
                         (["calme", "stress"], "exploratoire, hors famille, hors décision"))
        vide = r1.recompute_from_journal(*build_fixture(tempfile.mkdtemp(prefix="s2poolee_")),
                                         exclude_ranges=[(WS[0], WS[5])])
        self.assertEqual((vide["strates"], vide["poolee"]["z_pool"], vide["poolee"]["motif"]),
                         ({}, None, "aucune fenêtre complétée (n = 0)"))


class TestPooleeGardes(unittest.TestCase):
    """C-4 du cp-1 bref : chaque cas ⇒ z_pool non publié avec motif, jamais une valeur fabriquée."""
    OK = blk(176, 11, "0.0625", Decimal(0))

    def test_c4_i_une_strate_sous_la_garde(self):
        """Rougit si : garde ignorée (poolée publiée avec une strate non testée)."""
        po = r1.strate_poolee({"calme": self.OK, "stress": blk(20, 3, "0.1", None)})
        self.assertEqual((po["z_pool"], po["numerateur"], po["motif"]), (None, None, GARDE + "« stress »"))

    def test_c4_ii_strate_degeneree_variance_nulle(self):
        """Rougit si : dégénérée non distinguée ; garde ignorée (la variance de calme seule ferait un z)."""
        po = r1.strate_poolee({"calme": self.OK, "stress": blk(64, 0, "0", None, queue=False)})
        self.assertEqual((po["z_pool"], po["motif"]), (None, GARDE + "« stress »" + DEG))

    def test_c4_iii_deux_strates_degenerees_denominateur_nul(self):
        """Fixture d'exclusion (lectures toutes ok : P̂_more = 0 partout). Rougit si : garde ignorée
        (ValueError du dénominateur nul)."""
        po = r1.recompute_from_journal(*build_fixture(tempfile.mkdtemp(prefix="s2poolee_")))["poolee"]
        self.assertEqual((po["z_pool"], po["motif"]),
                         (None, GARDE + "« calme »" + DEG + " ; « stress »" + DEG))

    def test_c4_iv_v_une_seule_strate_n_nul(self):
        """n_s = 0 ⇔ strate absente : exclusion qui vide la strate stress. Rougit si : poolée publiée sur
        une seule strate (= z de la strate) ; cas pris pour une garde."""
        seule = "une seule strate au segment (« calme ») : la forme stratifiée somme au moins deux strates"
        self.assertEqual(r1.strate_poolee({"calme": self.OK})["motif"], seule)
        po = r1.recompute_from_journal(*build_fixture(tempfile.mkdtemp(prefix="s2poolee_")),
                                       exclude_ranges=[(WS[3], WS[5])])["poolee"]
        self.assertEqual((po["z_pool"], po["motif"]), (None, seule))


if __name__ == "__main__":
    unittest.main()
