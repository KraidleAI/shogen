"""Calendrier SB-5 (E-S-14, E-S-25 ; T-CAL-2) : instants epoch par `date -u -d … +%s` et valeurs écrites à la main,
et test croisé avec `window` de f35a70c (module chargé par chemin depuis s2-harness, après contrôle de son sha256, sans
import de shogen_s2) ; chaque test nomme les mutations qui le rougissent."""
import hashlib
import importlib.util
import math
import os
import time
import unittest
from fractions import Fraction

import aleas
import calendrier
import commun

CAL = commun.charger_parametres(environ={})["calendrier"]
WINDOW = os.path.join(commun.RACINE, "s2-harness", "shogen_s2", "window.py")
WINDOW_F35A70C = "f8c3b79f7f7893f343a00b6d6563cbbb502e2bd7af7888db958f895b5bc5fb94"   # git show f35a70c:… | sha256sum


class TestCalendrier(unittest.TestCase):
    def test_parametres_et_echelle(self):
        """E-S-25 : n_calme = 6 840·W, n_stress = 2 736·W, T_max = 1,5·W semaines (W = 16 : 109 440, 43 776 et 24
        semaines de 10 080 fenêtres, ADR l.158) ; lundi de référence 2026-12-07 00:00 UTC. Mutations M-5-01 (T_max sans
        le facteur 3/2), M-5-02 (n_s sur W − 1 semaines)."""
        self.assertEqual((CAL["w"], CAL["jours_stress"], CAL["lundi_reference"], CAL["echelle_semaines"], CAL["t_max"]),
                         (60, [5, 6], 1796601600, [12, 14, 16, 18, 20, 22, 24], [3, 2]))
        self.assertEqual(calendrier.echelle(CAL, 16), {"n": {"calme": 109440, "stress": 43776}, "t_max": 241920})
        self.assertEqual(calendrier.echelle(CAL, 12), {"n": {"calme": 82080, "stress": 32832}, "t_max": 181440})
        with self.assertRaises(commun.Refus) as c:
            calendrier.echelle(dict(CAL, t_max=[1, 11]), 1)
        self.assertEqual(c.exception.code, "CALENDRIER/t_max")

    def test_week_end_utc_t_cal_2(self):
        """Vendredi 2026-12-04 23:59, samedi 00:00, dimanche 23:59, lundi 2026-12-07 00:00 UTC, et l'époque (jeudi),
        sous TZ=JST-9 (vendredi 23:59 UTC y est samedi 08:59). Mutations M-CAL-3 (week-end en heure locale), M-5-03
        (époque prise pour un vendredi), M-5-04 (jours de stress inversés)."""
        tz = os.environ.get("TZ")
        os.environ["TZ"] = "JST-9"
        time.tzset()
        try:
            self.assertEqual([calendrier.strate(t, CAL) for t in (1796428740, 1796428800, 1796601540, 1796601600, 0)],
                             ["calme", "stress", "stress", "calme", "calme"])
            self.assertEqual([calendrier.jour_semaine(t) for t in (0, 345600, 1796601600, 1796428800)], [3, 0, 0, 5])
        finally:
            os.environ.pop("TZ") if tz is None else os.environ.update(TZ=tz)
            time.tzset()

    def test_croise_window_f35a70c(self):
        """Réplique contre window de f35a70c (sha256 épinglé) : jours de stress égaux à WEEKEND_STRATE_SPEC, jour et
        strate de chaque fenêtre de trois semaines, pour chacun des 7 jours de départ, égaux à weekday_utc et
        strate_from_spec. Mutation M-5-05 : blocs de journée décalés d'un jour."""
        with open(WINDOW, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), WINDOW_F35A70C)
        spec = importlib.util.spec_from_file_location("window_f35a70c", WINDOW)
        w = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(w)
        self.assertEqual(CAL["jours_stress"], w.WEEKEND_STRATE_SPEC["stress_weekdays"])
        for d in range(7):
            debut, n = CAL["lundi_reference"] + 86400 * d, 3 * 10080
            m = calendrier.masques(CAL, debut, n)
            for j in range(n):
                ws = debut + 60 * j
                self.assertEqual(calendrier.jour_semaine(ws), w.weekday_utc(ws))
                self.assertEqual("stress" if m["stress"] >> j & 1 else "calme",
                                 w.strate_from_spec(ws, w.WEEKEND_STRATE_SPEC))
            self.assertEqual(m["calme"] | m["stress"], (1 << n) - 1)

    def test_t_debut_tire(self):
        """T_début = lundi de référence 00:00 UTC + d jours, d uniforme sur 0..6 par seuils exacts k/7 (Q-S-08) ;
        référence un mardi, ou hors minuit : CALENDRIER/lundi. Mutations M-5-06 (six jours au lieu de sept), M-5-07
        (décalage en minutes au lieu de jours), M-5-13 (référence non contrôlée)."""
        s = aleas.seuil(Fraction(1, 7))
        u = (0.0, math.nextafter(s, 0.0), s, aleas.seuil(Fraction(6, 7)), math.nextafter(1.0, 0.0))
        self.assertEqual([calendrier.t_debut(CAL, iter([x]).__next__) for x in u],
                         [1796601600, 1796601600, 1796688000, 1797120000, 1797120000])
        for ref in (1796601600 + 86400, 1796601600 + 60):
            with self.assertRaises(commun.Refus) as c:
                calendrier.t_debut(dict(CAL, lundi_reference=ref), iter([0.0]).__next__)
            self.assertEqual(c.exception.code, "CALENDRIER/lundi")

    def test_masques_tronques_et_debut_de_journee(self):
        """Grille de 2 jours et 3 fenêtres depuis un vendredi : vendredi calme, samedi stress, puis 3 fenêtres de
        dimanche en stress ; aucun bit au-delà de T_max ; début hors minuit UTC : CALENDRIER/debut. Mutation M-5-08 :
        masques non tronqués à T_max."""
        m = calendrier.masques(CAL, 1796342400, 2 * 1440 + 3)
        self.assertEqual(m, {"calme": (1 << 1440) - 1, "stress": ((1 << 1443) - 1) << 1440})
        with self.assertRaises(commun.Refus) as c:
            calendrier.masques(CAL, 1796342400 + 60, 10)
        self.assertEqual(c.exception.code, "CALENDRIER/debut")
