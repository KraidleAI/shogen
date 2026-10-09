"""E1 câblée, SB-11j à SB-11l (E-S-38 ; Q-SI-8 (a) à (e) de SIM-INTEG ; points (6) et (8) de l'ajout daté du G0 du
2026-10-05 15:05:43 UTC ; REGIME-FAISABILITE-1) : attendus écrits à la main, produits par `bc -l`, ou recalculés ici
depuis un seul appel de calib_fiv.replication ; chaque test nomme les mutations qui le rougissent."""
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


def attendu(ep: dict, s: str, pt: tuple, f: Fraction, part: Fraction) -> dict:
    """REGIME-FAISABILITE-1 écrit ici à la main, hôte par hôte du format : panne, part x = f·p de la ligne « panne »
    d'ep, r_L = part·x, p_A = (x − r_L)/(1 − r_L) ; écart propre, p_A = f·(cellules d'écart − cellules de panne)/n_s ;
    r_E = p_A/(1 − φ + φκ), r′ = r_E(κ − 1)/(1 − r_E) ; maximum, [hôte, type] du premier maximum, verdict r′ < 1."""
    (phi, kappa, _t), rs = pt, []
    for h in HOTES:
        pa, ea = ep[s, h, "panne"], ep[s, h, "ecart"]
        x = f * Fraction(pa["cellules"], pa["n_s"])
        rl = part * x
        for j, pA in enumerate(((x - rl) / (1 - rl), f * Fraction(ea["cellules"] - pa["cellules"], pa["n_s"]))):
            re_ = pA / (1 - phi + phi * kappa)
            rs.append((re_ * (kappa - 1) / (1 - re_), h, ("panne", "ecart")[j]))
    m = max(rs, key=lambda y: y[0])
    return {"max": m[0], "ou": [m[1], m[2]], "faisable": m[0] < 1}


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

    def test_faisabilite_c1_c2(self):
        """REGIME-FAISABILITE-1 à C1 et à C2 sous le fond d'E1 (f = 1, aucune panne longue : e1.fond) et EP, sélection
        enveloppée (forcee : C1 = (1/100, 5, 60) et C2 = (1/10, 5, 60) en calme, l'inverse en stress) ; attendus de
        attendu(). Mutations M-11L-01 (point de C2 sous l'étiquette C1), M-11L-02 (f et part des pannes longues
        permutés au site d'appel), M-11L-07 (point d'une autre strate)."""
        with mock.patch.object(calib_fiv, "selection", side_effect=forcee):
            r = e1.calibrer(E1R, cal_e1(), fixture_e1(), None, {})
        for n, s, pt in (("C1", "calme", P0), ("C2", "calme", P), ("C1", "stress", P), ("C2", "stress", P0)):
            self.assertEqual(r["faisabilite"][n][s], attendu(EP, s, pt, Fraction(1), Fraction(0)), (n, s))

    def test_faisabilite_f_et_part(self):
        """REGIME-FAISABILITE-1 hors du fond d'E1 (f = 3/10, part des pannes longues 1/2), sur une EP synthétique de
        n_s = 1000 : en calme, l'hôte de rang k du format à 10 + k cellules de panne et une d'écart propre (la panne
        domine), au point (1/10, 5, 60) : faisable ; en stress, une cellule de panne et 120 + k d'écart propre (l'écart
        domine), au point (1/100, 50, 60) de la grille : p_A = 3/10 · 129/1000 au-dessus du seuil φ + (1 − φ)/κ =
        149/5000, infaisable ; attendus de attendu(). Mutations M-11L-03 (f ignoré), M-11L-04 (part longue appliquée à
        l'écart), M-11L-05 (part longue ignorée), M-11L-06 (verdict toujours faisable), M-11L-08 (types permutés),
        M-11L-09 (taux de panne pour l'écart), M-11L-10 (minimum au lieu du maximum)."""
        ep, f, part, q = {}, Fraction(3, 10), Fraction(1, 2), (Fraction(1, 100), Fraction(50), 60)
        for k, h in enumerate(HOTES):
            for s, pa, ec in (("calme", 10 + k, 11 + k), ("stress", 1, 121 + k)):
                ep[s, h, "panne"], ep[s, h, "ecart"] = {"cellules": pa, "n_s": 1000}, {"cellules": ec, "n_s": 1000}
        r = e1.faisabilite(PRM, ep, {"calme": P, "stress": q}, f, part)
        self.assertEqual(r, {"calme": attendu(ep, "calme", P, f, part), "stress": attendu(ep, "stress", q, f, part)})
        self.assertEqual([r[s]["faisable"] for s in ("calme", "stress")], [True, False])


    def test_faisabilite_cellules_et_grille(self):
        """REGIME-FAISABILITE-1, contrôle sur les cellules du §5.1 et les points de la grille (item, B.64 l.1067) :
        pour chaque cellule de cellules.nulles, à C1 et à C2 (sélection enveloppée), taux f·M de la cellule, M = plus
        grand multiplicateur de sa dérive (tendances, commune, sauts : 19/10 ; transitoire : 3 ; sinon 1 : forme de
        sources.Replication.union), part de ses pannes longues ; grille d'E1 sous son fond (f = 1, aucune panne
        longue), φ dans l'ordre inverse (1/10 puis 1/100) : r′ maximal sur les points et le point où il est atteint,
        par strate, jamais le premier point (garde d'attendu) ; attendus de attendu().
        Mutations M-11U-01 (multiplicateur de dérive ignoré), M-11U-02 (transitoire au multiplicateur des tendances),
        M-11U-03 (part longue de la cellule ignorée), M-11U-04 (point de C2 sous l'étiquette C1), M-11U-05 (grille :
        premier point au lieu du maximum)."""
        inv = dict(E1R, e1=dict(E1R["e1"], phi=E1R["e1"]["phi"][::-1]))
        with mock.patch.object(calib_fiv, "selection", side_effect=forcee):
            r = e1.calibrer(inv, cal_e1(), fixture_e1(), None, {})
        mult = {None: 1, "tendances": Fraction(19, 10), "commune": Fraction(19, 10), "sauts": Fraction(19, 10),
                "transitoire": Fraction(3), "initiale": 1}
        c1, c2 = {"calme": P0, "stress": P}, {"calme": P, "stress": P0}
        self.assertEqual(sorted(r["faisabilite_cellules"]), sorted(c["nom"] for c in PRM["cellules"]["nulles"]))
        for c in PRM["cellules"]["nulles"]:
            m = max(mult[x] for x in (c["derive"] or [None]))
            for n, pts in (("C1", c1), ("C2", c2)):
                for s in ("calme", "stress"):
                    self.assertEqual(r["faisabilite_cellules"][c["nom"]][n][s],
                                     attendu(EP, s, pts[s], Fraction(*c["f"]) * m, Fraction(*c["longues"])),
                                     (c["nom"], n, s))
        for s in ("calme", "stress"):
            g = [(attendu(EP, s, p, Fraction(1), Fraction(0))["max"], p) for p in calib_fiv.grille(inv)]
            self.assertNotEqual(max(g, key=lambda y: y[0])[1], g[0][1])
            self.assertEqual(r["faisabilite_grille"][s], list(max(g, key=lambda y: y[0])))

if __name__ == "__main__":
    unittest.main()
