"""Épisodes de panne et d'écart par unité, courbe FIV_série(ℓ). Attendus écrits à la main ; chaque test nomme la
mutation qui le rougit."""
import os
import unittest
from decimal import Decimal

import commun
import episodes
import regles
from tests import fixtures as fx

W = fx.W


class TestEpisodes(unittest.TestCase):
    def setUp(self):
        self.d = fx.dossier(self, "plan_episodes_")

    def test_episodes_coupes_par_une_fenetre_absente(self):
        """Positions 0 à 9, la 5 absente ; vrai en 0, 1, 2, 4, 6, 7, 9 : épisodes (3, censuré à gauche), (1, à droite),
        (2, à gauche), (1, à droite). Mutation ME-1 : suite comprimée (4 et 6, 7 fusionnés en un épisode de 3)."""
        fen = [(fx.VEN + W * i, i in (0, 1, 2, 4, 6, 7, 9)) for i in range(10) if i != 5]
        self.assertEqual(episodes.episodes(fen, W, bool), [(3, True, False), (1, False, True), (2, True, False),
                                                           (1, False, True)])

    def test_resume(self):
        """Longueurs 2 et 4 complètes, 1 censurée à droite, n_s = 8 : 3 épisodes, 7 cellules, taux 7/8 = 0.875, moyenne
        7/3, max 4, P50 au rang 2 : 2, P90 au rang 3 : 4 ; censurés 1 ; complets 2, moyenne 3. Mutation ME-2 : censure
        à droite non comptée (censurés 0, complets 3)."""
        r = episodes.resume([(2, False, False), (4, False, False), (1, False, True)], 8, [[50, 100], [90, 100]])
        self.assertEqual((r["episodes"], r["cellules"], r["taux"], r["max"], r["q"]), (3, 7, Decimal("0.875"), 4, [2, 4]))
        self.assertEqual((r["censures"], r["complets"], r["moyenne_complets"]), (1, 2, Decimal(3)))
        self.assertLess(abs(r["moyenne"] - Decimal(7) / Decimal(3)), Decimal("1E-25"))
        self.assertEqual(r["histogramme"], [(1, 1), (2, 1), (4, 1)])

    def test_courbe_fiv_serie(self):
        """I = 1, 1, 0, 0 consécutifs : écarts au centre ±1/2, γ̂₀ = 1, γ̂₁ = 1/4, γ̂₂ = −1/2 (sommes de produits) ; ℓ = 1 :
        FIV_série 1 ; ℓ = 2 : 1 + 1/4 = 1,25 ; ℓ = 3 : 1 + (4/3)(1/4) + (2/3)(−1/2) = 1 ; garde n ≥ 30·ℓ non tenue.
        Mutation ME-3 : ℓ − 1 passé à la variance (1 au lieu de 1,25)."""
        serie = [(fx.VEN + W * i, x) for i, x in enumerate((1, 1, 0, 0))]
        c = episodes.courbe(serie, W, [1, 2, 3])
        self.assertEqual([(x["ell"], x["n"], x["K"], x["FIV_serie"]) for x in c],
                         [(1, 4, 2, Decimal(1)), (2, 4, 2, Decimal("1.25")), (3, 4, 2, Decimal(1))])
        self.assertEqual([x["garde"] for x in c], [False] * 3)

    def test_controle_fiv_ecart_detecte(self):
        """FIV_série et K de la série recalculée comparés au bloc de compute_r1 à ℓ = 240. Mutation ME-5 : contrôle
        neutralisé (aucun écart rendu)."""
        par = {"calme": [(fx.VEN + W * i, {"a": fx.r1.Ecart.PANNE, "b": fx.r1.Ecart.PANNE if i == 0 else
                                           fx.r1.Ecart.PAS_ECART}, {}) for i in range(4)]}
        bon = {"strates": {"calme": {"K": 1, "bloc": {"FIV_serie": episodes.courbe(
            episodes.serie(par["calme"]), W, [240])[0]["FIV_serie"]}}}}
        faux = {"strates": {"calme": {"K": 1, "bloc": {"FIV_serie": Decimal(2)}}}}
        self.assertEqual((episodes.controle_fiv(par, {"base": bon, "w": W}), len(episodes.controle_fiv(
            par, {"base": faux, "w": W}))), ([], 1))

    def test_sortie_episodes_et_courbe(self):
        """10 fenêtres calmes, la 5 exclue (n = 9) ; a en panne en 0, 4, 6, 9 et périmé en 1 (ok 5 fois : 2·5 ≥ 9, gardé) ;
        b en panne en 0 ; x hors des unités, en panne sauf en 8 (au pool S2). a : pannes 1, 1, 1, 1 (toutes censurées),
        écarts 2, 1, 1, 1 ; série S2 : K = 5 (fenêtres 0, 1, 4, 6, 9) ; série D1-bis : K = 1 (fenêtre 0) ; FIV_série(1) =
        1 ; en-tête : sha256 de regles.py. Mutation ME-4 : unités prises au pool S2 de la strate (x imprimé) ; MC-13 :
        regles.py absent de l'en-tête."""
        ws = [fx.VEN + W * i for i in range(10)]
        fx.journaux(self.d, ws, lambda i, f: ("panne_transport" if (f == "a" and i in (0, 4, 6, 9)) or (f == "b" and i == 0)
                                              or (f == "x" and i != 8) else {"etat": "ok", "age": 200}
                                              if f == "a" and i == 1 else "ok"), list("abcdex"), sigma={"place": "100"})
        b = fx.r1.recompute_from_journal(*(os.path.join(self.d, n) for n in ("control.jsonl", "journal.jsonl")),
                                         [(ws[5], ws[5])], {"t0": ws[0], "n_fixe": 10})["strates"]["calme"]
        b3 = {"calme": (b["n"], b["K"], commun.dec(b["P_more"]))}
        r = fx.rendu(os.path.join(self.d, "r.out"), b3)
        p = fx.prm_fixture(list("abcde"), b3, commun.sha256(r), ws[0], 10, [(ws[5], ws[5])])
        p["fiv"] = {"ell": [1, 2]}
        s = os.path.join(self.d, "s.txt")
        rc = episodes.main(["--journaux", self.d, "--harnais", fx.HARNAIS, "--sortie", s, "--rendu", r,
                            "--parametres", fx.ecrire_prm(os.path.join(self.d, "p.json"), p)])
        with open(s, encoding="utf-8") as f:
            lignes = f.read().split(fx.NL)
        self.assertEqual((rc, b3["calme"][:2]), (0, (9, 5)))
        self.assertIn(f"regles.py sha256 {commun.sha256(regles.__file__)}", lignes[2])
        self.assertIn("    histogramme (longueur×nombre) : 1×4", lignes[lignes.index(next(
            x for x in lignes if x.startswith("  « calme » a (hôte ua) panne :"))) + 1])
        self.assertIn("    histogramme (longueur×nombre) : 1×3 2×1", lignes[lignes.index(next(
            x for x in lignes if x.startswith("  « calme » a (hôte ua) ecart :"))) + 1])
        self.assertTrue(any(x.startswith("  « calme » a (hôte ua) panne : n_s = 9 ; cellules = 4 ; épisodes = 4, dont "
                                         "censurés 4") for x in lignes))
        self.assertFalse(any(x.startswith("  « calme » x") for x in lignes))
        self.assertTrue(any(x.startswith("  S2 (D1) « calme » ℓ = 1 : n = 9 ; K = 5 ; FIV_série = 1 ;") for x in lignes))
        self.assertTrue(any(x.startswith("  D1-bis « calme » ℓ = 1 : n = 9 ; K = 1 ; FIV_série = 1 ;") for x in lignes))


if __name__ == "__main__":
    unittest.main()
