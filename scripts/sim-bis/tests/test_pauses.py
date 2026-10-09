"""Loi des pauses sur le masque (SB-11m), et celle du modèle à C1 à côté d'intervalles.txt (SB-11n) ; point (6)
de l'ajout daté du G0 du 2026-10-05 15:05:43 UTC : attendus écrits à la main, ou recomptés ici position par
position, segment par segment (forme indépendante des masques de bits) ; chaque test nomme les mutations qui le
rougissent."""
import functools
import unittest
from fractions import Fraction

import calib_fiv
import calibration
import commun
import e1

PRM = commun.charger_parametres(environ={})
EP = calibration.charger(PRM, environ={})["episodes"]
P = (Fraction(1, 10), Fraction(5), 60)
P0 = (Fraction(1, 100), Fraction(5), 60)
E1R = dict(PRM, e1=dict(PRM["e1"], phi=[[1, 100], [1, 10]], kappa=[5], tau_D=[60], replications=2,
                        cellule="E1-essai"))


@functools.lru_cache(maxsize=None)
def cal_e1():
    return calib_fiv.calendrier_e1(PRM, environ={})


def bits(*js):
    return sum(1 << j for j in js)


def naif(m: int, d: int) -> dict:
    """Recompte position par position : segments = suites de positions présentes ; dans chaque segment, suites de
    même valeur de d ; une suite qui touche un bout de son segment est censurée de ce côté."""
    out = {"completes": {}, "bord": {}, "complets": {}, "episodes": 0, "vides": 0, "segments": 0}
    j, n = 0, m.bit_length()
    while j < n:
        if not (m >> j) & 1:
            j += 1
            continue
        a = j
        while j < n and (m >> j) & 1:
            j += 1
        out["segments"] += 1
        k, suites = a, []
        while k < j:
            v, k0 = (d >> k) & 1, k
            while k < j and ((d >> k) & 1) == v:
                k += 1
            suites.append((v, k0 == a, k == j, k - k0))
        for v, g, f, lg in suites:
            if v:
                out["episodes"] += 1
            if v and not (g or f):
                out["complets"][lg] = out["complets"].get(lg, 0) + 1
            if not v:
                cle = "bord" if g or f else "completes"
                out[cle][lg] = out[cle].get(lg, 0) + 1
        out["vides"] += suites == [(0, True, True, j - a)]
    return out


class TestPauses(unittest.TestCase):
    def test_definitions_d_ep(self):
        """Positions présentes 0-3, 5-9, 12-13 ; d = 1 en 1, 2, 4 (absente), 6, 9 : épisodes (1-2) et (6) complets,
        (9) censuré à la fin ; pauses (0), (3), (5) de bord, (7-8) complète, segment 12-13 sans épisode ; d = 0 sur un
        segment : une pause de bord, segment sans épisode ; d = m : un épisode censuré, aucune pause (à la main).
        Mutations M-11M-01 (censure au début sans la position 0), M-11M-02 (pause complète à une censure),
        M-11M-03 (segment sans épisode à une censure), M-11M-04 (d hors des positions présentes)."""
        m = bits(0, 1, 2, 3, 5, 6, 7, 8, 9, 12, 13)
        self.assertEqual(e1.pauses(m, bits(1, 2, 4, 6, 9)),
                         {"completes": {2: 1}, "bord": {1: 3, 2: 1}, "complets": {2: 1, 1: 1}, "episodes": 3,
                          "vides": 1, "segments": 3})
        self.assertEqual(e1.pauses(bits(3, 4, 5), 0), {"completes": {}, "bord": {3: 1}, "complets": {}, "episodes": 0,
                                                       "vides": 1, "segments": 1})
        self.assertEqual(e1.pauses(bits(3, 4, 5), bits(3, 4, 5)),
                         {"completes": {}, "bord": {}, "complets": {}, "episodes": 1, "vides": 0, "segments": 1})
        self.assertEqual(e1.pauses(bits(0, 2), bits(2)), {"completes": {}, "bord": {1: 1}, "complets": {},
                                                          "episodes": 1, "vides": 1, "segments": 2})

    def test_rejeu_de_c1(self):
        """Réplications 0 et 1 de C1 rejouées (C1 = (1/100, 5, 60) en calme, (1/10, 5, 60) en stress, grille réduite
        sous les cellules E1-essai) : par strate et par hôte, pauses cumulées égales au recompte naif des séries D*(u)
        d'un appel indépendant de calib_fiv.replication par réplication, segments du masque comptés une fois.
        Mutations M-11M-05 (point de l'autre strate au site d'appel), M-11M-06 (réplication i + 1), M-11M-07 (états
        sur les positions générées au lieu du masque), M-11M-08 (segments sommés sur les réplications)."""
        cal, c1 = cal_e1(), {"calme": P0, "stress": P}
        r = e1.pauses_c1(E1R, EP, cal, c1, 1)
        self.assertEqual(sorted(r), ["calme", "stress"])
        for s, pt in c1.items():
            ref = {}
            for i in (0, 1):
                x = calib_fiv.replication(E1R, EP, cal, pt, calib_fiv.cellule(E1R, pt), i)
                for h, d in x["unites"][s].items():
                    y, z = naif(cal["presentes"][s], d), ref.setdefault(h, None)
                    if z is None:
                        ref[h] = y
                        continue
                    for k in ("completes", "bord", "complets"):
                        for lg, nb in y[k].items():
                            z[k][lg] = z[k].get(lg, 0) + nb
                    z["episodes"], z["vides"] = z["episodes"] + y["episodes"], z["vides"] + y["vides"]
            self.assertEqual(r[s], ref, s)

    def test_lignes_a_cote_d_intervalles(self):
        """Lignes du modèle à C1, puis la ligne « ecart » d'intervalles.txt de l'hôte et de la strate, recopiée avec
        son numéro (format à deux hôtes, texte synthétique) ; moyenne sous le contexte de r1, quantiles au rang le
        plus proche ⌈q·N/100⌉ ; aucune pause : « - » ; ligne absente ou en double : E1/intervalles (à la main).
        Mutations M-11M-09 (ligne « panne » au lieu de « ecart »), M-11M-10 (rang ⌊q·N/100⌋), M-11M-11 (moyenne sur
        les épisodes), M-11M-12 (histogramme des pauses de bord au lieu des complètes)."""
        prm = dict(PRM, calibration=dict(PRM["calibration"], unites=[["a", "fa"], ["b", "fb"]]))
        x = {"completes": {1: 2, 4: 1, 10: 1}, "bord": {3: 2}, "complets": {1: 5}, "episodes": 7, "vides": 1,
             "segments": 4}
        y = {"completes": {2: 1, 3: 2}, "bord": {}, "complets": {}, "episodes": 3, "vides": 0, "segments": 4}
        z = {"completes": {}, "bord": {5: 1}, "complets": {}, "episodes": 0, "vides": 1, "segments": 1}
        texte = commun.NL.join(["étiquette", "  « calme » fa (hôte a) panne : pauses complètes = 1",
                                "  « calme » fa (hôte a) ecart : pauses complètes = 9", "  « calme » fb (hôte b) ecart"
                                " : pauses complètes = 8", "  « stress » fa (hôte a) ecart : pauses complètes = 7",
                                "  « stress » fb (hôte b) ecart : pauses complètes = 6", ""])
        r = e1.lignes_pauses(prm, {"calme": {"a": x, "b": y}, "stress": {"a": z, "b": y}}, {"calme": P, "stress": P0},
                             2, texte)
        tete = "  modèle à C1 (φ = {}, κ = 5, τ_D = 60), « {} » {} (hôte {}), 2 réplications : pauses complètes = "
        self.assertEqual(r[1:], [
            tete.format("1/10", "calme", "fa", "a") + "4 ; segments = 4 ; épisodes = 7 (complets 5) ; moyenne = 4 ; "
            "max = 10 ; P50 = 1 ; P90 = 10 ; P99 = 10 ; pauses de bord = 2 (dont segments sans épisode 1)",
            "    histogramme des pauses (longueur×nombre) : 1×2 4×1 10×1",
            "    S2 (intervalles.txt l.3) : « calme » fa (hôte a) ecart : pauses complètes = 9",
            tete.format("1/10", "calme", "fb", "b") + "3 ; segments = 4 ; épisodes = 3 (complets 0) ; moyenne = "
            "2.6666666666666666666666666666666666666666666666667 ; max = 3 ; P50 = 3 ; P90 = 3 ; P99 = 3 ; pauses de "
            "bord = 0 (dont segments sans épisode 0)",
            "    histogramme des pauses (longueur×nombre) : 2×1 3×2",
            "    S2 (intervalles.txt l.4) : « calme » fb (hôte b) ecart : pauses complètes = 8",
            tete.format("1/100", "stress", "fa", "a") + "0 ; segments = 1 ; épisodes = 0 (complets 0) ; moyenne = - ; "
            "max = - ; P50 = - ; P90 = - ; P99 = - ; pauses de bord = 1 (dont segments sans épisode 1)",
            "    histogramme des pauses (longueur×nombre) : aucune pause",
            "    S2 (intervalles.txt l.5) : « stress » fa (hôte a) ecart : pauses complètes = 7",
            tete.format("1/100", "stress", "fb", "b") + "3 ; segments = 4 ; épisodes = 3 (complets 0) ; moyenne = "
            "2.6666666666666666666666666666666666666666666666667 ; max = 3 ; P50 = 3 ; P90 = 3 ; P99 = 3 ; pauses de "
            "bord = 0 (dont segments sans épisode 0)",
            "    histogramme des pauses (longueur×nombre) : 2×1 3×2",
            "    S2 (intervalles.txt l.6) : « stress » fb (hôte b) ecart : pauses complètes = 6"])
        self.assertTrue(r[0].startswith("[PAUSES À C1] "))
        for t in (texte.replace("fb (hôte b) ecart", "fb (hôte b) panne"),
                  texte + "  « stress » fb (hôte b) ecart : pauses complètes = 6" + commun.NL):
            with self.assertRaises(commun.Refus) as c:
                e1.lignes_pauses(prm, {"calme": {"a": x, "b": y}, "stress": {"a": z, "b": y}},
                                 {"calme": P, "stress": P0}, 2, t)
            self.assertEqual(c.exception.code, "E1/intervalles")


if __name__ == "__main__":
    unittest.main()
