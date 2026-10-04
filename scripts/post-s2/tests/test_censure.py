"""SHOGEN-CENSURE-INFO-2, bornes de z_s sous censure arbitraire : référence par énumération exhaustive de toutes les
imputations (chaque fenêtre sautée reçoit l'un des 2^N vecteurs de statuts), en arithmétique exacte, code écrit ici
sans le module testé. Chaque test nomme la mutation qui le rougit."""
import itertools
import tempfile
import unittest
from unittest import mock
from decimal import Decimal, localcontext
from fractions import Fraction

import censure
import commun
from tests import fixtures as fx

LUN = fx.VEN + 3 * 86400                         # 2026-08-31T00:00Z, lundi : 7 200 fenêtres calmes jusqu'au vendredi


def z_exact(n, k, e):
    """z = (K − n·P_more)/√(n·P_more·(1 − P_more)), P_more exact (Fraction), Decimal 60 chiffres à la fin."""
    p = [Fraction(x, n) for x in e]
    prod = lambda xs: 1 if not xs else xs[0] * prod(xs[1:])
    p0 = prod([1 - x for x in p])
    p1 = sum(p[i] * prod([1 - x for j, x in enumerate(p) if j != i]) for i in range(len(p)))
    pm = 1 - p0 - p1
    with localcontext() as c:
        c.prec = 60
        num, var = Decimal(k) - Decimal(n) * Decimal(pm.numerator) / pm.denominator, n * pm * (1 - pm)
        return num / (Decimal(var.numerator) / var.denominator).sqrt()


def enumeration(n, k, e, s):
    """Toutes les imputations de s fenêtres sautées : (min, max, valeur au témoin « tout en écart »)."""
    vals = []
    for vecs in itertools.product(itertools.product((0, 1), repeat=len(e)), repeat=s):
        ep = [x + sum(v[i] for v in vecs) for i, x in enumerate(e)]
        vals.append(z_exact(n + s, k + sum(sum(v) >= 2 for v in vecs), ep))
    return min(vals), max(vals), z_exact(n + s, k + s, [x + s for x in e])


class TestCensureBornes(unittest.TestCase):
    def test_maximum_exact_et_borne_inferieure_exterieure(self):
        """n = 40, K = 1, e = (4, 2, 1), s = 2 (condition de concavité tenue pour c ≤ 2) : maximum égal à celui de
        l'énumération ; borne inférieure ≤ minimum de l'énumération ; témoin « tout en écart » égal à sa valeur
        énumérée. Rougit si : sommets à un seul flux ; c limité à 0 ; gradient ≤ 1/n' omis (borne trop haute)."""
        bas, haut, tout = enumeration(40, 1, [4, 2, 1], 2)
        b = censure.bornes(40, 1, [4, 2, 1], 2)
        self.assertEqual(b["relachees"], [])
        self.assertLess(abs(b["max"] - haut), Decimal("1e-40"))
        self.assertLess(abs(b["temoin_min"] - tout), Decimal("1e-40"))
        self.assertLessEqual(b["borne_inf"], bas + Decimal("1e-40"))

    def test_maximum_sur_une_paire_non_voisine(self):
        """Correction G2 C-2 : n = 40, K = 1, e = (4, 1, 2), s = 2 : maximum de l'énumération atteint au seul sommet
        c = 2, flux 0 et 2 (non voisins) : e' = (6, 1, 4), K' = 3, P_more = 115/6174, z' = 13692/√29264970
        ≈ 2,5310041 (à la main). Rougit si les sommets « deux flux à c » sont limités aux paires voisines (≈ 2,4407)."""
        _bas, haut, _tout = enumeration(40, 1, [4, 1, 2], 2)
        b = censure.bornes(40, 1, [4, 1, 2], 2)
        with localcontext() as c:
            c.prec = 60
            a_la_main = Decimal(13692) / Decimal(29264970).sqrt()
        self.assertEqual((b["relachees"], b["argmax"]), ([], (2, (0, 2))))
        self.assertLess(max(abs(b["max"] - haut), abs(b["max"] - a_la_main)), Decimal("1e-40"))

    def test_condition_non_tenue_borne_relachee_reste_exterieure(self):
        """n = 6, e = (2, 1, 1), s = 3 : condition fausse pour c ≥ 1 : c marqués, et la borne haute reste ≥ maximum de
        l'énumération (512 imputations). Rougit si la borne relâchée n'est pas appliquée (sommet seul)."""
        bas, haut, _tout = enumeration(6, 1, [2, 1, 1], 3)
        b = censure.bornes(6, 1, [2, 1, 1], 3)
        self.assertTrue(b["relachees"])
        self.assertGreaterEqual(b["max"] + Decimal("1e-40"), haut)
        self.assertLessEqual(b["borne_inf"], bas + Decimal("1e-40"))

    def test_borne_serree_sans_ecart_d_arrondi(self):
        """Constat de l'exécution (journal G1 §3) : borne inférieure et témoin « tout en écart » égaux en droit (même P
        rationnel à c = s) mais différents au dernier chiffre (représentations entières non réduites). Entrées publiées
        de la strate stress (docs/11 §3.5 et §2.6 ; aucun journal lu). Rougit si la fraction n'est pas réduite."""
        b = censure.bornes(11397, 133, [46, 11, 46, 6, 7, 39, 21, 51, 127, 226, 113], 2094)
        self.assertEqual((b["borne_inf"] == b["temoin_min"], b["serree"]), (True, True))


class TestCensureTemoins(unittest.TestCase):
    def test_temoins_et_lecture_non_identifie(self):
        """7 200 positions calmes, une sur 72 sans marqueur (i ≡ 70 mod 72 : s = 100, la dernière est vue) ; a, b, c
        en panne chacun seul sur 180 positions : K = 0. Témoin « toutes propres » : z_s < 0, NE REJETTE PAS ; témoin
        W_B : REJETTE ; lecture « non identifié ». Attendu métamorphique : les journaux imputés de W_A, de W_B et d'une
        imputation fixe, écrits sur disque, rendent par le chargeur (r1.compute_r1) et r1.regle_critere les mêmes n, K,
        z_s, z_bloc et la même valeur. Rougit si : positions sautées mal recomptées ; série complétée sans les positions
        sautées propres ; W_B qui n'impute qu'un écart par fenêtre ; lecture forcée."""
        d = tempfile.mkdtemp(prefix="pp_censure_")
        grille = [LUN + 60 * i for i in range(7200)]
        vues = [w for i, w in enumerate(grille) if i % 72 != 70]
        vu = set(vues)

        def panne(w, f):                          # a, b, c en panne seuls : positions [200k ; 200k + 180)
            return f in "abc" and 200 * "abc".index(f) <= (w - LUN) // 60 < 200 * "abc".index(f) + 180
        fx.journaux(d, vues, lambda i, f: "panne_transport" if panne(vues[i], f) else "ok")
        res = censure.identification(commun.charger(d, {"t0": LUN, "n_fixe": len(vues)}, [(0, 0)]))
        x = res["strates"]["calme"]
        self.assertEqual((x["s"], len(x["pos"]), x["K"], x["controle"]), (100, 100, 0, True))
        self.assertEqual((res["wa"]["calme"]["valeur"], res["wb"]["calme"][2]["valeur"]), ("NE REJETTE PAS", "REJETTE"))
        self.assertEqual(res["lecture"], "non identifié sous censure arbitraire")
        c, paire, t = res["wb"]["calme"]
        fixe = {p: (0, 1) for p in x["pos"][::2]}         # imputation fixe : 50 positions, a et b en écart
        for imput, tem in (({}, res["wa"]["calme"]), ({p: paire for p in x["pos"][::x["s"] // c][:c]}, t),
                           (fixe, censure.temoin(x, fixe, 60, 10))):
            fx.ecrire(d, [fx.params(), *(fx.marqueur(w) for w in grille)], [
                fx.lecture(w, f, "panne_transport" if (panne(w, f) and w in vu) or (w in imput and fx.POOL.index(f) in
                                                                                         imput[w]) else "ok")
                for w in grille for f in fx.POOL])
            b = commun.charger(d, {"t0": LUN, "t_fin": grille[-1] + 60}, [(0, 0)])["base"]["strates"]["calme"]
            v = commun.r1.regle_critere({"strates": {"calme": b}})["strates"]["calme"]["valeur"]
            self.assertEqual((b["n"], b["K"], b["z"], b["bloc"]["z_bloc"], v),
                             (tem["n"], tem["K"], tem["z"], tem["z_bloc"], tem["valeur"]))

    def test_sans_fenetre_sautee_lecture_non_etablie(self):
        """s = 0 : aucun témoin W_B, lecture « identification non établie par cette construction » ; un s du harnais
        différent des positions recomptées ferme la strate. Rougit si la lecture « non identifié » est rendue sans deux
        témoins de valeurs différentes, ou si le contrôle des positions est inopérant."""
        d = tempfile.mkdtemp(prefix="pp_censure0_")
        fx.journaux(d, [LUN + 60 * i for i in range(30)], lambda i, f: "panne_transport" if f in "ab" and i % 5 == 0
                    else "ok")
        dd = commun.charger(d, {"t0": LUN, "n_fixe": 30}, [(0, 0)])
        res = censure.identification(dd)
        self.assertEqual((res["strates"]["calme"]["s"], res["wb"], res["lecture"]),
                         (0, {}, "identification non établie par cette construction"))
        with mock.patch.object(censure.r1, "fenetres_sautees", lambda *a, **k: {"calme": 1}):
            res = censure.identification(dd)             # s du harnais ≠ positions recomptées : strate non traitée
        self.assertEqual((res["strates"]["calme"]["controle"], res["wa"]), (False, {}))


if __name__ == "__main__":
    unittest.main()
