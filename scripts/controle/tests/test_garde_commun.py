"""Cas de garde_commun.py (lot GARDE-FOUS-ORCH ; G0 docs/adr-0028/G0-lots-DETTES.md, ajout GF-0), rouges sur l'erreur
réelle reproduite, verts sur le cas sain. GF-1 : horloge et heures. E14 : vers 04:18 et 04:22 écrits à 04:14 ; le
2026-10-02 : une heure écrite 19:5x. L'horloge est fixée par un faux `date` dans le PATH, jamais par une variable."""
import os
import tempfile
import unittest
from datetime import datetime, timezone
from unittest import mock

import garde_commun as gc

NL = chr(10)
H = datetime(2026, 10, 10, 4, 14, tzinfo=timezone.utc)      # E14 : il était 04:14:00


def codes(texte, horloge=H):
    return [(n, c) for n, c, _x in gc.horodatages_fautifs(texte, horloge)]


class Heures(unittest.TestCase):
    def test_e14_heures_futures(self):
        """E14 : refus du mandataire daté vers 04:18 et page des actes datée 04:22, écrits à 04:14 : deux refus."""
        texte = NL.join(["Refus du mandataire le 2026-10-10 vers 04:18 UTC.", "Page des actes, 2026-10-10 04:22."])
        self.assertEqual(codes(texte), [(1, "heure-future"), (2, "heure-future")])
        self.assertEqual(gc.horodatages_fautifs(texte, H)[1][2], "2026-10-10 04:22")

    def test_heure_approchee(self):
        """2026-10-02 : 19:5x écrit hors guillemets ; 21:2x et 19:xx aussi ; 19:50 et 1:5x (pas une heure) non."""
        texte = NL.join(["le 2026-10-02 vers 19:5x UTC", "à 21:2x puis 19:xx", "à 19:50, version 1:5x"])
        self.assertEqual(codes(texte), [(1, "heure-approchee"), (2, "heure-approchee"), (2, "heure-approchee")])

    def test_borne_tolerance(self):
        """Tolérance de 120 s : 04:16 et 04:16:00 admis à 04:14:00, 04:16:01 refusé ; secondes lues."""
        self.assertEqual(codes("2026-10-10 04:16 et 2026-10-10 04:16:00 et 2026-10-10T04:13:59Z"), [])
        self.assertEqual(codes("le 2026-10-10 à 04:16:01"), [(1, "heure-future")])

    def test_autres_jours(self):
        """Une date d'un autre jour n'est pas jugée (échéance, veille) ; la date la plus proche de l'heure compte."""
        self.assertEqual(codes("2026-10-11 09:00 ; 2026-10-09 23:59"), [])
        self.assertEqual(codes("du 2026-10-09 au 2026-10-10 04:22"), [(1, "heure-future")])

    def test_exemptions(self):
        """Mot de plan dans les 40 caractères d'avant, code et guillemets français : rien n'est jugé."""
        g, d = chr(171), chr(187)
        texte = NL.join(["prévu le 2026-10-10 05:00", "jalon : 2026-10-10 05:00", "`2026-10-10 05:00` et `19:5x`",
                         g + " écrit le 2026-10-10 05:00, vers 19:5x " + d])
        self.assertEqual(codes(texte), [])

    def test_horloge_lue_par_date_u(self):
        """L'horloge vient de `date -u` (faux `date` en tête du PATH), jamais de l'horloge de Python."""
        with tempfile.TemporaryDirectory() as d:
            faux = os.path.join(d, "date")
            with open(faux, "w", encoding="utf-8") as f:
                f.write(NL.join(["#!/bin/sh", 'if [ "$1" = -u ]; then echo 2031-02-03T04:05:06Z;',
                                 "else echo 2031-02-03T09:09:09Z; fi", ""]))
            os.chmod(faux, 0o755)
            with mock.patch.dict(os.environ, {"PATH": d + os.pathsep + os.environ.get("PATH", "")}):
                self.assertEqual(gc.maintenant(), datetime(2031, 2, 3, 4, 5, 6, tzinfo=timezone.utc))
