"""Contribution de la paire de flux OKX à K de S2 (SHOGEN-R1-HOTE-STRUCTUREL-1). Attendus écrits à la main ; chaque
test nomme la mutation qui le rougit."""
import os
import unittest

import commun
import okx
from tests import fixtures as fx

POOL = ["okx_ticker", "okx_index", "a", "b", "c"]
PANNES = {0: {"okx_ticker": "panne_transport", "okx_index": "panne_transport"},
          1: {"okx_ticker": "panne_transport", "okx_index": "panne_transport", "a": "panne_transport"},
          2: {"okx_index": "panne_http", "a": "panne_transport"},
          3: {"a": "panne_transport", "b": "panne_transport"},
          4: {"okx_ticker": "panne_transport", "okx_index": "panne_http"},
          6: {"okx_ticker": "panne_transport"}}


def journaux(d):
    ws = [fx.VEN + fx.W * i for i in range(10)]
    fx.journaux(d, ws, lambda i, f: PANNES.get(i, {}).get(f, "ok"), POOL)
    return ws


def prm(ws, b3, sha):
    p = fx.prm_fixture(POOL, b3, sha, ws[0], 10)
    p["pool_d1bis"]["unites"] = {"okx": "okx_ticker", "ua": "a", "ub": "b", "uc": "c"}
    return p


class TestOkx(unittest.TestCase):
    def setUp(self):
        self.d = fx.dossier(self, "plan_okx_")

    def test_comptes_de_la_paire(self):
        """n = 10, K = 5 (fenêtres 0 à 4) ; co-écart des deux flux en 0, 1, 4, tous dans K, types (panne, panne) ; les deux
        en panne_transport en 0 et 1 ; pertes à m = 2 : paire fusionnée en 0 et 4, sans okx_index en 0, 2, 4, sans
        okx_ticker en 0 et 4 ; écarts 4 et 4. Mutation MO-1 : perte de la fusion comptée sans « m = 2 » (3) ; MO-2 :
        panne_transport lue sur okx_ticker seul (3)."""
        ws = journaux(self.d)
        d = commun.charger(self.d, prm(ws, {}, "-"))
        c = okx.comptes(commun.classer(d, d["pools_s2"])["calme"], "okx_ticker", "okx_index", d["rmap"])
        self.assertEqual({k: c[k] for k in ("n", "K", "paire", "K_paire", "K_paire_pt", "perte_hote", "perte_index",
                                            "perte_ticker", "ecarts_tk", "ecarts_ix")},
                         {"n": 10, "K": 5, "paire": 3, "K_paire": 3, "K_paire_pt": 2, "perte_hote": 2, "perte_index": 3,
                          "perte_ticker": 2, "ecarts_tk": 4, "ecarts_ix": 4})
        self.assertEqual(dict(c["types"]), {("panne", "panne"): 3})

    def test_flux_absent_du_pool_de_la_strate(self):
        """okx_index absent du classement (retiré par D1) : aucune paire, aucune perte liée à lui. Mutation MO-4 : accès
        direct à la cellule absente (KeyError)."""
        r1 = fx.r1
        fen = [(fx.VEN, {"okx_ticker": r1.Ecart.PANNE, "a": r1.Ecart.PANNE}, {})]
        c = okx.comptes(fen, "okx_ticker", "okx_index", {})
        self.assertEqual((c["K"], c["paire"], c["perte_index"], c["perte_ticker"], c["ecarts_ix"]), (1, 0, 0, 1, 0))

    def test_sortie(self):
        """Rendu de la fixture : n = 10, K = 5, p̂ = (0,4 ; 0,4 ; 0,3 ; 0,1 ; 0) : P0 = 0,2268, P1 = 0,4248, P̂_more =
        0,3484 (à la main). K paire fusionnée 3, sans okx_index 2, sans okx_ticker 3 ; pool D1-bis (okx_ticker, a, b, c ;
        okx_ticker ok 6 fois, gardé) : K = 2 (fenêtres 1 et 3). Mutation MO-3 : K du pool D1-bis pris au pool S2 (5)."""
        ws = journaux(self.d)
        b3 = {"calme": (10, 5, "0.3484")}
        r = fx.rendu(os.path.join(self.d, "r.out"), b3)
        s = os.path.join(self.d, "s.txt")
        rc = okx.main(["--journaux", self.d, "--harnais", fx.HARNAIS, "--sortie", s, "--rendu", r, "--parametres",
                       fx.ecrire_prm(os.path.join(self.d, "p.json"), prm(ws, b3, commun.sha256(r)))])
        with open(s, encoding="utf-8") as f:
            texte = f.read()
        self.assertEqual(rc, 0)
        for attendu in ("« calme » : n = 10 ; K (pool S2 du rendu) = 5 ; écarts : okx_ticker 4, okx_index 4 fenêtres ; "
                        "co-écart des deux flux : 3 fenêtres, dont 3 dans K",
                        "  K si la paire compte pour une unité (écart si l'un des deux flux l'est) = 3 (contribution de la "
                        "paire : 2 fenêtres, fraction de K 0.4)",
                        "  K sans okx_index (classement inchangé) = 2 ; K sans okx_ticker = 3",
                        "  K sur le pool D1-bis (médiane leave-one-out et retraits D1-bis appliqués) = 2 (n = 10)"):
            self.assertIn(fx.NL + attendu + fx.NL, texte)


if __name__ == "__main__":
    unittest.main()
