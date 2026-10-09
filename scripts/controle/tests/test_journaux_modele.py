"""Cas de enforcement/journaux-modele.py (lot DETTES-T3, DT3-B ; SHOGEN-R1-FORME-RESOLUE-1, adjudication Q-B1) :
ligne « - **Modèle** : `<id>` » des journaux G1/G2 nouveaux, identifiant de la liste blanche du lint R-1 ou suivi de
[1m], égalité exacte ; journaux versés à 0cfbe3e exemptés par nom et sha256. Arbres temporaires, sauf le dernier cas."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SCRIPT = os.path.join(RACINE, "enforcement", "journaux-modele.py")
NL = chr(10)


def controler(racine):
    p = subprocess.run([sys.executable, "-B", SCRIPT, racine], capture_output=True, text=True, timeout=60)
    return p.returncode, p.stderr


class JournauxModele(unittest.TestCase):
    def arbre(self, fichiers):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)
        os.makedirs(os.path.join(d, "docs"))
        for nom, texte in fichiers.items():
            with open(os.path.join(d, "docs", nom), "w", encoding="utf-8") as f:
                f.write(texte)
        return d

    def test_nouveaux_conformes(self):
        """Identifiant de la liste blanche, ou suivi de [1m], suivi ou non d'un texte : conforme."""
        code, err = controler(self.arbre({
            "G1-lot-NEUF.md": "# G1" + NL + "- **Modèle** : `claude-opus-5-5` (identifiant exact), effort max" + NL,
            "G2-lot-NEUF.md": "# G2" + NL + "- **Modèle** : `claude-opus-5-5[1m]`" + NL,
            "G1-lot-NEUF2.md": "- **Modèle** : `claude-sonnet-5-5`" + NL,
            "G2-lot-NEUF3.md": "- **Modèle** : `claude-fable-5-1`" + NL,
            "G2-lot-NEUF4.md": "- **Modèle** : `claude-haiku-5-5`" + NL}))
        self.assertEqual(code, 0, err)

    def test_g2_sans_ligne_refuse(self):
        code, err = controler(self.arbre({"G2-lot-NEUF.md": "# G2" + NL + "Modèle résolu : `claude-opus-5-5`" + NL}))
        self.assertEqual(code, 1, err)
        self.assertIn("G2-lot-NEUF.md : 0 ligne(s)", err)

    def test_formes_refusees(self):
        """Banni, préfixe, tier nu, casse de [1m], [1m] hors liste ou répété, sans accents graves, texte collé, deux
        lignes : refus."""
        for ligne in ("- **Modèle** : `claude-opus-5`", "- **Modèle** : `claude-opus-5-5-x`", "- **Modèle** : `opus`",
                      "- **Modèle** : `claude-opus-5-5[1M]`", "- **Modèle** : `claude-opus-5[1m]`",
                      "- **Modèle** : `opus[1m]`", "- **Modèle** : `claude-opus-5-5[1m][1m]`",
                      "- **Modèle** : claude-opus-5-5",
                      "- **Modèle** : `claude-opus-5-5`, effort max", "- **Modèle** :`claude-opus-5-5`",
                      "- **Modèle** : `claude-opus-5-5`" + NL + "- **Modèle** : `claude-opus-5-5`"):
            with self.subTest(ligne=ligne):
                code, err = controler(self.arbre({"G1-lot-NEUF.md": "# G1" + NL + ligne + NL}))
                self.assertEqual(code, 1, err)
                self.assertIn("G1-lot-NEUF.md", err)

    def test_exempte_puis_modifie(self):
        """Journal versé, sans ligne « Modèle » de cette forme : exempté tel quel, refusé dès qu'un octet change."""
        with open(os.path.join(RACINE, "docs", "G1-lot-CORR.md"), encoding="utf-8") as f:
            texte = f.read()
        self.assertEqual(controler(self.arbre({"G1-lot-CORR.md": texte}))[0], 0)
        self.assertEqual(controler(self.arbre({"G1-lot-NEUF.md": texte}))[0], 1)      # mêmes octets, nom neuf
        self.assertEqual(controler(self.arbre({"G1-lot-D8a.md": texte}))[0], 1)       # mêmes octets, autre exempté
        code, err = controler(self.arbre({"G1-lot-CORR.md": texte + "ajout" + NL}))
        self.assertEqual(code, 1, err)
        self.assertIn("G1-lot-CORR.md : 0 ligne(s)", err)

    def test_racine_illisible(self):
        self.assertEqual(controler(os.path.join(tempfile.gettempdir(), "absente-journaux-modele"))[0], 3)
        d = self.arbre({"G1-lot-NEUF.md": "- **Modèle** : `claude-opus-5-5`" + NL})
        self.assertEqual(subprocess.run([sys.executable, "-B", SCRIPT, d, d], capture_output=True,
                                        timeout=60).returncode, 3)                    # deux racines : erreur
        for outil in ("", "def auteur_admis(:" + NL, "import module_absent_de_journaux_modele" + NL):
            with self.subTest(outil=outil):       # DT3-F : outil vide, en erreur de syntaxe, à import manquant
                d = self.arbre({"G1-lot-NEUF.md": "- **Modèle** : `claude-opus-5-5`" + NL})
                os.makedirs(os.path.join(d, "s2-harness", "tools"))
                os.makedirs(os.path.join(d, "enforcement"))
                shutil.copy(SCRIPT, os.path.join(d, "enforcement"))
                with open(os.path.join(d, "s2-harness", "tools", "oracle_record.py"), "w", encoding="utf-8") as f:
                    f.write(outil)
                self.assertEqual(subprocess.run([sys.executable, "-B", os.path.join(d, "enforcement",
                                 "journaux-modele.py"), d], capture_output=True, timeout=60).returncode, 3)

    def test_arbre_du_depot(self):
        """Journaux du dépôt : conformes (un journal nouveau sans la ligne fait rougir ce cas)."""
        code, err = controler(RACINE)
        self.assertEqual(code, 0, err)
