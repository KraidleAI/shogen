"""Cas de presg5.py (lot GARDE-FOUS-ORCH) : pré-contrôle S-G5 versé à l'octet (GF-2), puis rendu outil (GF-2b : sorties
0, 1, 3, interdits jamais ouverts). E9 : versement refusé par S-G5, messages d'outils anglais entre guillemets
français. Sortie dorée : SHA_DOREE est le sha256 de la sortie de l'outil d'origine (scratchpad, sha256 60de4077…87ef0)
sur FIXTURE, mesuré avant le versement. Les guillemets français sont posés à l'exécution (<< et >>) : ce fichier n'en
porte aucun autour d'un texte anglais. L'outil tourne en sous-processus (-X dev -W error -I -B)."""
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest

import garde_commun as gc

PRESG5 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "presg5.py")
LONG = ("This is a deliberately long sentence that is not in the corpus and that is written to check that the "
        "printed fragment is cut at one hundred and sixty characters by the tool")
FIXTURE = {
    "biblio/INDEX.md": "# Index\nThe quick evaluation of the method is robust to noise.\nrobust to the noise\n"
                       "state of the art methods are not always the best\n",
    "biblio/page.html": "<p>This is the <b>reference</b> text of the paper.</p>\n",
    "biblio/source.txt": "We show that the estimator is consistent with the data.\n"
                         "git status shows the state of the tree\n",
    "biblio/note.sidecar": "It's been shown that the effect is not random.\n",
    "biblio/image.pdf": "%PDF the hidden text is not in the corpus\n",
    "a.md": "Message : << fatal: not a git repository (or any of the parent directories) >>.\n"
            "Registre : << The quick evaluation of the method is robust to noise. >>\n"
            "Balises : << This is the reference text of the paper >>\n"
            "Coupure : << We show that [...] consistent with the data >>\n"
            "Apostrophe : << It’s been shown that the effect is not random >>\n"
            "Un mot : << nothing is here today >> ; bornes << it is the best >> et << it is the worst >>\n"
            "Tirets : << state-of-the-art methods are not always the best >>\n"
            "Français : << une citation française qui ne compte pas >>\n"
            "Code : << `git status` shows the state of the tree >>\n"
            "Crochets : << the method is [abcdefghijklmnopqrstuvwxyz01234] robust to the noise >>\n"
            "PDF : << the hidden text is not in the corpus >>\n"
            "Deux lignes : << This line has\nno match in the corpus at all >>\n"
            "Long : << " + LONG + " >>\n",
}
SHA_DOREE = "b2b708c81d100fdb6ddcb37b85311b51e33be48ba454abe8687b44e91eb40502"
E9 = "fatal: not a git repository (or any of the parent directories"


def batir(d, fichiers=FIXTURE):
    for chemin, texte in fichiers.items():
        os.makedirs(os.path.dirname(os.path.join(d, chemin)) or d, exist_ok=True)
        with open(os.path.join(d, chemin), "w", encoding="utf-8", newline="") as f:
            f.write(texte.replace("<<", chr(171)).replace(">>", chr(187)))


def lancer(d, *fichiers):
    p = subprocess.run([sys.executable, "-X", "dev", "-W", "error", "-I", "-B", PRESG5, *fichiers], cwd=d,
                       capture_output=True, timeout=120)
    return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace")


class Presg5(unittest.TestCase):
    def test_sortie_doree_et_contrat(self):
        """Mêmes lignes que l'outil d'origine sur FIXTURE (sha256 épinglé) ; fragment introuvable : sortie 1."""
        with tempfile.TemporaryDirectory() as d:
            batir(d)
            code, sortie, erreur = lancer(d, ".", "a.md")
        self.assertEqual((code, hashlib.sha256(sortie).hexdigest(), erreur), (1, SHA_DOREE, ""), sortie[-300:])

    def test_e9_message_d_outil(self):
        """E9 : message d'outil anglais entre guillemets français, absent de biblio/ : sortie 1, ligne nommée."""
        with tempfile.TemporaryDirectory() as d:
            batir(d)
            batir(d, {"e9.md": "Refus : << " + E9 + ") >>\n"})
            code, sortie, _ = lancer(d, ".", "e9.md")
        attendu = ["e9.md:1: " + chr(171) + " " + E9 + " " + chr(187), "presg5 : 1 fragment(s) introuvable(s)"]
        self.assertEqual((code, sortie.decode("utf-8").splitlines()), (1, attendu))

    def test_sain_sortie_0(self):
        with tempfile.TemporaryDirectory() as d:
            batir(d)
            batir(d, {"ok.md": "<< The quick evaluation of the method is robust to noise. >> << it is the best >>\n"})
            self.assertEqual(lancer(d, ".", "ok.md")[:2], (0, b"presg5 : 0 fragment(s) introuvable(s)\n"))

    def test_erreurs_sortie_3(self):
        """Sans fichier, biblio/INDEX.md absent, ou fichier sous un interdit (jamais ouvert, jamais nommé) : 3."""
        with tempfile.TemporaryDirectory() as d:
            batir(d, {"a.md": "<< the hidden text is not in the corpus >>\n"})
            self.assertEqual(lancer(d, ".", "a.md")[0], 3)
            batir(d)
            self.assertEqual(lancer(d, ".")[0], 3)
            batir(d, {"docs/rapports/x.md": "<< the hidden text is not in the corpus >>\n"})
            code, sortie, erreur = lancer(d, ".", "docs/rapports/x.md")
        self.assertEqual((code, sortie), (3, b""))
        self.assertIn("interdit", erreur)
        self.assertNotIn("x.md", erreur)

    def test_biblio_interdit_non_lu(self):
        """Un fichier de biblio/ au nom d'une pièce de D.2 n'est jamais lu : la citation qu'il porterait reste
        introuvable (nom pris dans fm11.py, jamais écrit ici ni affiché)."""
        m = next(r.pattern for r in gc.interdits()[1] if r.pattern.replace("-", "").isalnum())
        with tempfile.TemporaryDirectory() as d:
            batir(d)
            batir(d, {"biblio/" + m + ".txt": "the secret sentence is in this file\n",
                      "c.md": "<< the secret sentence is in this file >>\n"})
            self.assertEqual(lancer(d, ".", "c.md")[0], 1)
