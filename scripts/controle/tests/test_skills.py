"""Cas des skills du lot GARDE-FOUS-ORCH (GF-10) : .claude/skills/shogen-avant-*/SKILL.md, un par moment de l'acte.
Chaque skill porte un en-tête name (nom du dossier) et description, en français ; il donne des commandes : chaque
sous-commande de avant_acte.py et chaque chemin de scripts/controle/ qu'il cite existent, les options exigées de chaque
sous-commande citée y paraissent ; il nomme les erreurs visées ; il ne porte ni marqueur de dette nu ni clé model."""
import argparse
import os
import re
import unittest

import avant_acte

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SKILLS = ("shogen-avant-lancer", "shogen-avant-committer", "shogen-avant-pousser", "shogen-avant-ecrire")
DETTE = re.compile("(TO" + "DO|FIX" + "ME)")


def lire(nom):
    with open(os.path.join(RACINE, ".claude", "skills", nom, "SKILL.md"), encoding="utf-8") as f:
        return f.read()


class Skills(unittest.TestCase):
    def test_en_tete(self):
        """En-tête entre deux lignes ---, name égal au dossier, description de forme commune (moment, commandes),
        aucune clé model."""
        for nom in SKILLS:
            lignes = lire(nom).split(chr(10))
            fin = lignes.index("---", 1)
            entete = lignes[1:fin]
            self.assertEqual((lignes[0], [x for x in entete if x.startswith("name:")]), ("---", ["name: " + nom]), nom)
            description = " ".join(x.strip() for x in entete if not x.startswith(("name:", "description:")))
            self.assertIn("description: >-", entete, nom)
            forme = description.startswith("Garde-fous de Shōgen à appliquer") and "commandes" in description
            self.assertTrue(forme, nom)
            self.assertFalse(any("model" in x for x in entete), nom)

    def test_commandes_et_chemins(self):
        """Chaque sous-commande de avant_acte.py citée existe ; chaque chemin scripts/controle/ cité existe ; chaque
        skill nomme ses erreurs et cite au moins une commande ; aucun marqueur de dette nu."""
        for nom in SKILLS:
            texte = lire(nom)
            commandes = re.findall("avant_acte[.]py(?: --depot [^ ]+)? ([a-z]+)", texte)
            self.assertTrue(commandes, nom)
            self.assertEqual([c for c in commandes if c not in avant_acte.COMMANDES], [], nom)
            sous = [x for x in avant_acte.parseur()._actions if isinstance(x, argparse._SubParsersAction)][0].choices
            for c in commandes:
                requis = [o for x in sous[c]._actions if x.required for o in x.option_strings]
                self.assertEqual([o for o in requis if o not in texte], [], (nom, c))
            chemins = re.findall("scripts/controle/[A-Za-z0-9_./-]*[A-Za-z0-9_]", texte)
            self.assertEqual([c for c in chemins if not os.path.exists(os.path.join(RACINE, c))], [], nom)
            self.assertRegex(texte, "Erreurs visées : E[0-9]+", nom)
            self.assertIsNone(DETTE.search(texte), nom)
