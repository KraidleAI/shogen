"""Cas de presg5.py (lot GARDE-FOUS-ORCH, GF-2) : pré-contrôle S-G5 versé à l'octet depuis le scratchpad de
l'orchestrateur (erreurs E9 et E10). Sortie dorée : SHA_DOREE est le sha256 de la sortie de l'outil d'origine (sha256
60de4077…87ef0) sur FIXTURE, mesuré avant le versement. Les guillemets français sont posés à l'exécution (<< et >>) :
ce fichier n'en porte aucun autour d'un texte anglais. L'outil tourne en sous-processus (-I -B)."""
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest

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


def batir(d, fichiers=FIXTURE):
    for chemin, texte in fichiers.items():
        os.makedirs(os.path.dirname(os.path.join(d, chemin)) or d, exist_ok=True)
        with open(os.path.join(d, chemin), "w", encoding="utf-8", newline="") as f:
            f.write(texte.replace("<<", chr(171)).replace(">>", chr(187)))


def lancer(d, *fichiers):
    p = subprocess.run([sys.executable, "-I", "-B", PRESG5, *fichiers], cwd=d, capture_output=True, timeout=120)
    return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace")


class Presg5(unittest.TestCase):
    def test_sortie_doree_et_contrat(self):
        """Lignes de l'outil d'origine sur FIXTURE (sha256 épinglé) ; il sort toujours en 0."""
        with tempfile.TemporaryDirectory() as d:
            batir(d)
            code, sortie, erreur = lancer(d, ".", "a.md")
        self.assertEqual((code, hashlib.sha256(sortie).hexdigest(), erreur), (0, SHA_DOREE, ""), sortie[-300:])
