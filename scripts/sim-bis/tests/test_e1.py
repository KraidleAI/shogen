"""E1 câblée, SB-11j et SB-11k (E-S-38 ; Q-SI-8 (a) à (e) de SIM-INTEG ; points (6) et (8) de l'ajout daté du G0 du
2026-10-05 15:05:43 UTC) : attendus écrits à la main, produits par `bc -l`, ou recalculés ici depuis un seul appel de
calib_fiv.replication ; chaque test nomme les mutations qui le rougissent."""
import copy
import functools
import json
import os
import shutil
import tempfile
import unittest
from decimal import Decimal
from fractions import Fraction
from unittest import mock

import calib_fiv
import calibration
import commun
import e1
import executer

PRM = commun.charger_parametres(environ={})
K_ = PRM["calibration"]
EP = calibration.charger(PRM, environ={})["episodes"]
HOTES = [h for h, _f in K_["unites"]]
P = (Fraction(1, 10), Fraction(5), 60)
E1R = dict(PRM, e1=dict(PRM["e1"], phi=[[1, 100], [1, 10]], kappa=[5], tau_D=[60], replications=2,
                        cellule="E1-essai"))
P0 = (Fraction(1, 100), Fraction(5), 60)
VRAIE = calib_fiv.selection


@functools.lru_cache(maxsize=None)
def cal_e1():
    """Calendrier d'E1 (masque mesuré de PLAN-S2BIS-2), lu une fois."""
    return calib_fiv.calendrier_e1(PRM, environ={})


@functools.lru_cache(maxsize=None)
def fixture_e1():
    """E1 réduite (C0 et deux points, φ = 1/100 et 1/10, κ = 5, τ_D = 60 ; deux réplications), sous des cellules
    « E1-essai-… », jamais celles d'E1 (discipline d'E-4 : aucune valeur d'E1 vue avant E0) : {point : moyennes_point
    des enregistrements relus en JSON}."""
    out = {}
    for p in [None] + calib_fiv.grille(E1R):
        out[p] = e1.moyennes_point([executer.jsonable(e1.replication_e1(E1R, EP, cal_e1(), p, i)) for i in (0, 1)], K_)
    return out


def code_de(f, *a):
    """Code du refus nommé levé par f(*a), nom de l'exception sinon, None sans exception (rouge d'assertion)."""
    try:
        f(*a)
    except commun.Refus as e:
        return e.code
    except Exception as e:                                          # noqa: BLE001 (rouge d'assertion, jamais d'erreur)
        return type(e).__name__
    return None


def forcee(*a):
    """calib_fiv.selection enveloppée : C1 = P0 et C2 = P en calme, l'inverse en stress (points de la grille réduite),
    le reste du constat inchangé : C1 ≠ C2, et C1 diffère d'une strate à l'autre."""
    x = VRAIE(*a)
    x["calme"].update(C1=P0, C2=P)
    x["stress"].update(C1=P, C2=P0)
    return x


class TestReplicationE1(unittest.TestCase):
    def test_courbes_d_un_seul_appel(self):
        """Q-SI-8 (a) et (e) : réplications 0 et 1 du point (1/10, 5, 60) : un seul appel de calib_fiv.replication
        par réplication ; courbe de I_t et courbes des dix hôtes du format sur le masque de chaque strate, égales aux
        FIV exacts de calib_fiv.courbe des séries rendues par cet appel ; le lot du point (cellule E1-essai-1_10-5-60,
        [0, 2)) porte ces enregistrements. Mutations M-11J-01 (hôtes d'une autre réplication), M-11J-02 (I_t sur les
        positions générées au lieu du masque), M-11J-03 (deux appels), M-11J-04 (courbes sur l ≠ calibration.ell)."""
        cal, ell = cal_e1(), K_["ell"]
        for i in (0, 1):
            with mock.patch.object(calib_fiv, "replication", wraps=calib_fiv.replication) as m:
                r = e1.replication_e1(E1R, EP, cal, P, i)
            self.assertEqual(m.call_count, 1)
            x = calib_fiv.replication(E1R, EP, cal, P, "E1-essai-1_10-5-60", i)
            self.assertEqual(sorted(r["strates"]), sorted(x["strates"]))
            for s, (pos, val) in x["strates"].items():
                self.assertEqual(r["strates"][s]["I"], [c["fiv"] for c in calib_fiv.courbe(pos, val, ell, K_)], s)
                self.assertEqual(sorted(r["strates"][s]["unites"]), sorted(HOTES), s)
                for h, d in x["unites"][s].items():
                    attendu = [c["fiv"] for c in calib_fiv.courbe(pos, d, ell, K_)]
                    self.assertEqual(r["strates"][s]["unites"][h], attendu, (s, h))
            if i == 1:
                d = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
                self.addCleanup(shutil.rmtree, d)
                c, _h = e1.lot_e1(E1R, EP, cal, P, (1, 2), 1, d, ["e"])
                self.assertEqual(os.path.basename(c), "E1-essai-1_10-5-60.000001-000002.lot")
                with open(c, "rb") as f:
                    lot = json.loads(f.read().split(commun.NL.encode(), 1)[1])
                self.assertEqual(lot["enregistrements"], [executer.jsonable(r)])

    def test_moyennes_point(self):
        """Agrégation d'un point (enregistrements relus, chaînes JSON) : I_t = 1, 2 ; 2, 4 ; indéfinie : moyenne exacte
        3/2, 3, une indéfinie ; variance exacte des définies, dénominateur m − 1 : 1/2, 2 ; écart-type par Decimal.sqrt
        sous le contexte de r1 : √(1/2), √2 (bc -l, à 10⁻⁴⁹ près) ; une seule définie : variance et écart-type None.
        Hôtes : a = 1, 2 ; 3, 4 ; 1/2, 1 : 3/2, 7/3, aucune indéfinie ; b défini une fois sur trois : deux indéfinies
        (Q-SI-8 (d)). Mutations M-11J-05 (variance au dénominateur m), M-11J-06 (indéfinies comptées pour 0), M-11J-07
        (racine sous le contexte par défaut)."""
        def r(i, ii, a, b):
            return {"i": i, "strates": {"calme": {"I": ii, "unites": {"a": a, "b": b}}}}
        n = [None, None]
        m = e1.moyennes_point([r(0, ["1", "2"], ["1", "2"], n), r(1, ["2", "4"], ["3", "4"], ["1", "1"]),
                               r(2, n, ["1/2", "1"], n)], K_)["calme"]
        self.assertEqual((m["I"], m["variance"]), ({"fiv": [Fraction(3, 2), 3], "definies": 2, "indefinies": 1},
                                                  [Fraction(1, 2), 2]))
        for x, ref in zip(m["ecart_type"], ("0.707106781186547524400844362104849039284835937688474036588339",
                                            "1.414213562373095048801688724209698078569671875376948073176679")):
            self.assertLess(abs(x - Decimal(ref)), Decimal("1E-49"))
        self.assertEqual(m["unites"], {"a": {"fiv": [Fraction(3, 2), Fraction(7, 3)], "definies": 3, "indefinies": 0},
                                       "b": {"fiv": [1, 1], "definies": 1, "indefinies": 2}})
        m = e1.moyennes_point([r(0, ["1", "2"], ["1", "2"], n), r(1, n, ["1", "2"], n)], K_)["calme"]
        self.assertEqual((m["variance"], m["ecart_type"]), ([None, None], [None, None]))


II = ("dans la strate {}, la famille E1 n'atteint pas les FIV_u mesurés ; C1 y est une borne basse de la mesure, et « "
      "borne haute » ne s'applique pas")


class TestCalibrer(unittest.TestCase):
    def test_selection_par_charger_unites_q_si_8_b(self):
        """Q-SI-8 (b) : C1, C2 et constat de bord égaux à calib_fiv.selection sur la cible EP (pool D1-bis), les
        moyennes de I_t et des hôtes, et les FIV_u lus par calibration.charger_unites(prm, cal["presentes"], ep) ;
        masque retouché (première position de calme retirée) : CALIB/croisement, que analyser_unites ne donnerait pas.
        Mutations M-11K-01 (analyser_unites au lieu de charger_unites), M-11K-02 (positions générées au lieu des
        positions présentes), M-11K-03 (cible du pool S2 (D1) au lieu d'e1.pool)."""
        moy, cal = fixture_e1(), cal_e1()
        r = e1.calibrer(E1R, cal, moy, None, {})
        ep = calibration.charger(PRM, environ={})
        u = calibration.charger_unites(PRM, cal["presentes"], ep["episodes"], environ={})
        a = calib_fiv.selection(E1R, {s: ep["fiv"]["D1-bis", s] for s in ("calme", "stress")},
                                {p: {s: m[s]["I"] for s in m} for p, m in moy.items()}, u,
                                {p: {s: m[s]["unites"] for s in m} for p, m in moy.items() if p})
        for s in ("calme", "stress"):
            self.assertEqual([r["strates"][s][k] for k in ("C1", "C2", "bord", "residus")],
                             [a[s][k] for k in ("C1", "C2", "bord", "residus")], s)
        c = cal["presentes"]["calme"]
        faux = dict(cal, presentes=dict(cal["presentes"], calme=c & ~(c & -c)))
        self.assertEqual(code_de(e1.calibrer, E1R, faux, moy, None, {}), "CALIB/croisement")

    def test_bord_et_phrases_q_si_8_c(self):
        """(8)(iv) et Q-SI-8 (c) : ligne [BORD E1] de chaque strate (calib_fiv.ligne_bord de son constat) ; grille
        réduite (τ_D = 60 extrême) : les deux strates au bord, phrases (8)(ii) de chaque strate et (8)(iii), écrites à
        la main ; calme hors du bord : phrase (8)(ii) du stress seule. Mutations M-11K-04 (phrase (8)(iii) sans
        C1-calme au bord), M-11K-05 (ligne d'une autre strate), M-11K-10 (phrase (8)(ii) sans condition de bord)."""
        r = e1.calibrer(E1R, cal_e1(), fixture_e1(), None, {})
        iii = ("[BORD E1] (8)(iii) : si W*(C1) ≤ 16 et que C1-calme est au bord, le paquet dit que les 16 semaines "
               "reposent sur un niveau que la famille ne peut pas dépasser : information à l'investisseur à l'accord "
               "A-1 de S-2, sans question ; si W*(C1) > 16, A-2 porte la même phrase ; les trois W* sont imprimés "
               "(SB-12)")
        self.assertEqual(r["phrases"], [f"[BORD E1] (8)(ii) « {s} » : " + II.format(s) for s in ("calme", "stress")]
                         + [iii])
        for s in ("calme", "stress"):
            self.assertEqual(r["strates"][s]["ligne_bord"], calib_fiv.ligne_bord(s, r["strates"][s]["bord"]), s)
        sel = {"calme": {"bord": {"au_bord": False}}, "stress": {"bord": {"au_bord": True}}}
        self.assertEqual(e1.phrases_bord(sel), ["[BORD E1] (8)(ii) « stress » : " + II.format("stress")])

    def test_impressions_par_hote(self):
        """Point (6) et Q-SI-8 (d) : sélection enveloppée (forcee : C1 ≠ C2, strates distinctes) ; par strate et par
        hôte, résidus ln F̄_u,C1(ℓ) − ln F_u(ℓ) aux ℓ retenus (garde de fiv_unites.txt, F_u défini), recalculés ici par
        Decimal.ln ; point qui minimiserait Q₁ pour l'hôte seul (calib_fiv.q1 réduit à l'hôte, égalités par
        calib_fiv._rang ; diagnostic) ; réplications à FIV indéfini de chaque point. Mutations M-11K-06 (résidus à C2),
        M-11K-07 (ℓ non gardés), M-11K-08 (point de Q₁ maximal), M-11K-09 (indéfinies de I_t sous l'étiquette d'un
        hôte), M-11K-11 (résidus de signe inversé)."""
        moy, cal = fixture_e1(), cal_e1()
        with mock.patch.object(calib_fiv, "selection", side_effect=forcee):
            r = e1.calibrer(E1R, cal, moy, None, {})
        ctx = calib_fiv.contexte(K_)
        ep = calibration.charger(PRM, environ={})
        u = calibration.charger_unites(PRM, cal["presentes"], ep["episodes"], environ={})
        for s, c1 in (("calme", P0), ("stress", P)):
            self.assertEqual(r["strates"][s]["C1"], c1)
            for h in HOTES:
                fu, mb = u[s][h], moy[c1][s]["unites"][h]["fiv"]
                js = [j for j, c in enumerate(fu) if c["garde"] and c["fiv"] is not None]
                def ln(x):
                    return ctx.divide(Decimal(x.numerator), Decimal(x.denominator)).ln(ctx)
                res = [[K_["ell"][j], ctx.subtract(ln(mb[j]), ln(fu[j]["fiv"]))] for j in js]
                x = r["strates"][s]["unites"][h]
                self.assertEqual(len(x["residus_C1"]), len(res), (s, h))
                for (e_, v), (e2, w) in zip(x["residus_C1"], res):
                    self.assertEqual(e_, e2)
                    self.assertLess(abs(v - w), Decimal("1E-45"), (s, h, e_))
                q = [(calib_fiv.q1({h: moy[p][s]["unites"][h]}, {h: fu}, K_["ell"], ctx), p)
                     for p in calib_fiv.grille(E1R)]
                self.assertEqual(x["point_Q1"], min((y for y in q if y[0] is not None), key=calib_fiv._rang)[1])
                self.assertEqual(x["indefinies"], {calib_fiv.cellule(E1R, p): moy[p][s]["unites"][h]["indefinies"]
                                                   for p in calib_fiv.grille(E1R)})
        m2 = copy.deepcopy(moy)
        m2[P]["calme"]["unites"]["okx"]["indefinies"] = 7
        x = e1.calibrer(E1R, cal, m2, None, {})["strates"]["calme"]["unites"]["okx"]["indefinies"]
        self.assertEqual(x["E1-essai-1_10-5-60"], 7)


if __name__ == "__main__":
    unittest.main()
