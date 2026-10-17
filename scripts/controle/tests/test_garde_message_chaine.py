"""Cas de SHOGEN-GARDE-CROCHET-MESSAGE-CHAINE-1 (GARDE-FOUS phase 3, groupe B ; annexe B, B.108 ; G2 du groupe A) :
faits_et_appels lit un message humain sous ses deux formes (content chaîne, content liste de blocs) ; une chaîne
découpée caractère par caractère cachait à R5 l'identifiant et le compte que l'humain avait écrits. Crochet chargé par
son chemin, joué en processus sur un journal synthétique (nom en .txt) d'un dossier temporaire."""
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GARDE = os.path.join(RACINE, ".claude", "hooks", "garde_faits.py")
NL = chr(10)
MESSAGE = "Reprends le lot à 4f3e2d1 : 7 tests verts."      # identifiant et compte fictifs, tapés par l'humain


def charger():
    spec = importlib.util.spec_from_file_location("garde_faits_mc", GARDE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MessageChaine(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.t, self.g = t.name, charger()

    def jouer(self, contenu, texte):
        """(sortie, stderr) du crochet sur un Write de BRIEF-x.md après un message humain de contenu `contenu`."""
        j = os.path.join(self.t, "journal.txt")
        with open(j, "w", encoding="utf-8") as f:
            f.write(json.dumps({"type": "user", "message": {"role": "user", "content": contenu}}) + NL)
        e = {"hook_event_name": "PreToolUse", "transcript_path": j, "cwd": self.t, "tool_name": "Write",
             "tool_input": {"file_path": os.path.join(self.t, "BRIEF-x.md"), "content": texte}}
        err = io.StringIO()
        with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(e))), contextlib.redirect_stderr(err):
            try:
                code = self.g.main()
            except SystemExit as x:
                code = x.code
        return code, err.getvalue()

    def test_r5_voit_le_message_a_contenu_chaine(self):
        """Message humain à contenu chaîne : R5 y voit l'identifiant et le compte (permis) ; même message en liste de
        blocs : permis ; message qui ne les porte pas : refus R5 (identifiant, puis compte du brief)."""
        blocs = [{"type": "text", "text": MESSAGE}]
        for contenu in (MESSAGE, blocs):
            self.assertEqual(self.jouer(contenu, "Base 4f3e2d1 ; 7 tests."), (0, ""), contenu)
            self.assertEqual(self.jouer(contenu, "Attendu : 7 tests."), (0, ""), contenu)
        code, err = self.jouer("Reprends le lot.", "Base 4f3e2d1 ; 7 tests.")
        self.assertEqual((code, "R5" in err, "4f3e2d1" in err), (2, True, True), err)
        code, err = self.jouer("Reprends le lot.", "Attendu : 7 tests.")
        self.assertEqual((code, "R5" in err, "7 tests" in err), (2, True, True), err)
        refus = "Stop hook feedback:" + NL + "GARDE-FAITS : REFUS. R5 : 4f3e2d1 jamais affiché."     # G2, C-2
        for contenu in (refus, [{"type": "text", "text": refus}]):      # un refus du crochet n'est pas un texte humain
            self.assertEqual(self.jouer(contenu, "Base 4f3e2d1.")[0], 2, contenu)

    def test_faits_et_appels_deux_formes(self):
        """Les deux formes donnent le même texte humain, entier (jamais un caractère par entrée)."""
        for contenu in (MESSAGE, [{"type": "text", "text": MESSAGE}]):
            humain = self.g.faits_et_appels([{"type": "user", "message": {"content": contenu}}])[3]
            self.assertEqual(humain, [MESSAGE], contenu)


if __name__ == "__main__":
    unittest.main()
