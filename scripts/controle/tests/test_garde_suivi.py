"""Cas du suivi des diffs reçus (lot GARDE-FOUS-ORCH, phase 2, groupe A ; annexe B, B.102,
SHOGEN-GARDE-OUTIL-E6-E7-E12-E13-1 ; erreur E13 : correctif DT5-24, test dont la troisième valeur ne testait rien,
README des contrôles non mis à jour), dans un dépôt git temporaire isolé (tests/aide_garde.py)."""
import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

import avant_acte
from tests import aide_garde as ag

NL = chr(10)


class Suivi(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.tmp = t.name
        self.d, self.env = ag.depot(self.tmp, {"scripts/controle/README.md": "# Outils" + NL,
                                               "scripts/controle/x.py": "import re" + NL,
                                               "scripts/controle/tests/test_x.py": "import unittest" + NL,
                                               "biblio/INDEX.md": "# index" + NL})      # corpus de presg5 (.md)
        env = mock.patch.dict(os.environ, self.env, clear=True)
        env.start()
        self.addCleanup(env.stop)

    def diff_de(self, fichiers, *options):
        ag.ecrire(self.d, fichiers)
        texte = ag.git(self.d, self.env, "diff")
        ag.git(self.d, self.env, "checkout", "--", ".")
        chemin = os.path.join(self.tmp, "x.diff")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(texte)
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(io.StringIO()):
            code = avant_acte.main(["--depot", self.d, "diff", "--fichier", chemin, *options])
        return code, [x.split(" ; à faire")[0] for x in sortie.getvalue().split(NL)[:-1]]

    def rapport(self, texte):
        chemin = os.path.join(self.tmp, "RAPPORT.md")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(texte)
        return chemin

    def test_e13_readme_des_controles(self):
        """E13 : fonction publique ajoutée à scripts/controle/x.py, absente du README : refus D3 ; nommée par le même
        diff : conforme ; privée, ou hors de scripts/controle/ : non jugée."""
        fonction = {"scripts/controle/x.py": "import re" + NL + "def borne_temps(x):" + NL + "    return x" + NL}
        self.assertEqual(self.diff_de(fonction), (1, ["REFUS D3 : scripts/controle/x.py:2 : fonction publique "
                                                      "borne_temps absente de scripts/controle/README.md (E13)"]))
        readme = {"scripts/controle/README.md": "# Outils" + NL + "Ajout : `borne_temps(x)`." + NL}
        self.assertEqual(self.diff_de({**fonction, **readme}), (0, []))
        prive = {"scripts/controle/x.py": "import re" + NL + "def _aide(x):" + NL + "    return x" + NL,
                 "scripts/autre.py": "def publique():" + NL + "    pass" + NL}
        self.assertEqual(self.diff_de(prive), (0, []))

    def test_e13_test_sans_mutant_tue(self):
        """E13 : test ajouté sans rapport : refus D4 ; rapport qui ne le dit pas tué (vivant, ou absent) : refus ;
        ligne du rapport qui le nomme avec un mutant tué : conforme ; test modifié (def inchangée) : non jugé."""
        test = {"scripts/controle/tests/test_x.py": "import unittest" + NL + "class T(unittest.TestCase):" + NL
                + "    def test_temps_borne(self):" + NL + "        pass" + NL}
        self.assertEqual(self.diff_de(test), (1, ["REFUS D4 : 1 test(s) ajouté(s), aucun rapport de mutants (--rapport) "
                                                  "(E13)"]))
        vivant = self.rapport("| M-1 | test_temps_borne | vivant |" + NL + "| M-2 | test_autre | tué |" + NL)
        self.assertEqual(self.diff_de(test, "--rapport", vivant), (1, ["REFUS D4 : scripts/controle/tests/test_x.py:3 : "
                                                                       "test_temps_borne sans mutant tué au rapport (E13)"]))
        self.assertEqual(self.diff_de(test, "--rapport", self.rapport("| M-1 | test_temps_borne | tué |" + NL)), (0, []))
        self.assertEqual(self.diff_de({"scripts/controle/tests/test_x.py": "import unittest  # suite" + NL}), (0, []))

    def test_d3_mot_commun(self):
        """SHOGEN-GARDE-D3-MOT-COMMUN-1 (annexe B, B.108) : fonction suivi ajoutée, README qui ne porte suivi que comme
        mot courant (non suivi), dans un autre mot (`suivis`, poursuivi(x)) ou dans un passage de code : refus D3 ;
        nommée en code (`suivi`, `avant_acte.suivi`) ou en signature (suivi(a, f)) : conforme."""
        fonction = {"scripts/controle/x.py": "import re" + NL + "def suivi(a, f):" + NL + "    return a" + NL}
        refus = (1, ["REFUS D3 : scripts/controle/x.py:2 : fonction publique suivi absente de scripts/controle/README.md "
                     "(E13)"])
        for texte in ("Un chemin non suivi est refusé.", "Voir `suivis` et `le suivi des diffs`x.", "poursuivi(x)."):
            readme = {"scripts/controle/README.md": "# Outils" + NL + texte + NL}
            self.assertEqual(self.diff_de({**fonction, **readme}), refus, texte)
        for texte in ("D3 : `suivi`, contrôle du README.", "Signature : suivi(a, fichiers), non suivi.",
                      "Voir `avant_acte.suivi`."):
            readme = {"scripts/controle/README.md": "# Outils" + NL + texte + NL}
            self.assertEqual(self.diff_de({**fonction, **readme}), (0, []), texte)
