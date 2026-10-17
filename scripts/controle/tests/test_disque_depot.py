"""Cas de SHOGEN-GARDE-DISQUE-DU-DEPOT-1 (GARDE-FOUS phase 3, groupe B ; annexe B, B.108 ; G2 du groupe C) : la
sous-commande disque (et le contrôle de disque du modèle de chaîne, qui l'appelle avec --depot) mesure le système de
fichiers du dépôt, et celui de TMPDIR s'il en diffère, jamais / par défaut. Espace libre fixé par un double de
os.statvfs (par chemin), système de fichiers de TMPDIR par un double de os.stat limité à ce chemin."""
import os
import unittest
from unittest import mock

from tests import test_avant_acte as ta

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
REEL_VFS, REEL_STAT = os.statvfs, os.stat


class DisqueDuDepot(ta.Depot):
    def setUp(self):
        super().setUp()
        self.autre = os.path.join(self.tmp, "autre")
        os.makedirs(self.autre)
        os.environ["TMPDIR"] = self.autre

    def doubles(self, gio, autre_systeme=False):
        """os.statvfs : gio[chemin] Gio libres (100 ailleurs, / compris) ; os.stat : TMPDIR sur un autre système de
        fichiers si autre_systeme."""
        def vfs(p):
            r = REEL_VFS(p)
            libre = int(gio.get(os.path.realpath(p), 100) * 2 ** 30)
            return os.statvfs_result((r.f_bsize, 1, 2 ** 50, 2 ** 50, libre, r.f_files, r.f_ffree, r.f_favail,
                                      r.f_flag, r.f_namemax))

        def stat(p, *a, **k):
            s = REEL_STAT(p, *a, **k)
            if autre_systeme and isinstance(p, str) and os.path.realpath(p) == os.path.realpath(self.autre):
                return os.stat_result(tuple(s[:2]) + (s.st_dev + 1,) + tuple(s[3:10]))
            return s
        pile = [mock.patch.object(os, "statvfs", vfs), mock.patch.object(os, "stat", stat)]
        for p in pile:
            p.start()
            self.addCleanup(p.stop)

    def test_disque_du_depot(self):
        """Dépôt à 2,9 Gio libres, / à 100 : refus DQ qui nomme le dépôt (l'ancien contrôle lisait / : conforme) ; à
        7 Gio : conforme ; TMPDIR sur le même système : une seule mesure, même à 2,9 Gio sur son chemin."""
        d = os.path.realpath(self.d)
        self.doubles({d: 2.9})
        code, sortie = self.lancer("disque")
        self.assertEqual((code, sortie.count("REFUS DQ"), d in sortie), (1, 1, True), sortie)
        self.doubles({d: 7, os.path.realpath(self.autre): 2.9})
        self.assertEqual(self.lancer("disque"), (0, ""))

    def test_tmpdir_sur_un_autre_systeme(self):
        """TMPDIR sur un autre système de fichiers, à 2,9 Gio libres, dépôt à 7 : refus DQ qui nomme TMPDIR ; --min-go
        serre les deux mesures."""
        autre = os.path.realpath(self.autre)
        self.doubles({os.path.realpath(self.d): 7, autre: 2.9}, autre_systeme=True)
        code, sortie = self.lancer("disque")
        self.assertEqual((code, sortie.count("REFUS DQ"), autre in sortie), (1, 1, True), sortie)
        self.doubles({os.path.realpath(self.d): 7, autre: 7}, autre_systeme=True)
        self.assertEqual(self.lancer("disque")[0], 0)
        self.assertEqual(self.lancer("disque", "--min-go", "8")[1].count("REFUS DQ"), 2)

    def test_modele_de_chaine_passe_le_depot(self):
        """Le modèle de chaîne contrôle le disque par acte disque, et acte passe --depot "$DEPOT" à avant_acte.py.
        Intégration P3 (I-5 de la G2 du groupe B) : le point 1 de la skill shogen-avant-lancer appelle disque avec
        --depot, non df -h /."""
        with open(os.path.join(RACINE, "scripts", "controle", "gabarits", "chaine.sh"), encoding="utf-8") as f:
            texte = f.read()
        self.assertIn('acte() { "$PYTHON" -I -B "$OUTILS/avant_acte.py" --depot "$DEPOT" "$@"; }', texte)
        self.assertIn('acte disque --min-go "${DISQUE_MIN_GO:-0}"', texte)
        with open(os.path.join(RACINE, ".claude", "skills", "shogen-avant-lancer", "SKILL.md"), encoding="utf-8") as f:
            skill = f.read()
        self.assertEqual(("avant_acte.py --depot <dépôt> disque" in skill, "df -h /" in skill), (True, False))


if __name__ == "__main__":
    unittest.main()
