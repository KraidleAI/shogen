"""Cas du journal des refus du crochet GARDE-FAITS (GARDE-FOUS phase 3, annexe B, B.108 : phase 3 de
SHOGEN-GARDE-FOUS-ORCH-1) : une ligne par refus et par passage, acte abrégé sans secret, en-tête unique. Le crochet du
dépôt est lancé tel quel sur des journaux synthétiques (nom en .txt), son journal des refus dans un dossier temporaire
(SHOGEN_GARDE_REFUS), l'heure fixée par un faux date en tête du PATH."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GARDE = os.path.join(RACINE, ".claude", "hooks", "garde_faits.py")
NL, TAB = chr(10), chr(9)
H = "2026-10-16T10:00:00Z"
ENTETE = TAB.join(["heure", "evenement", "regle", "acte", "agent"]) + NL


class Base(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.t, self.j = t.name, os.path.join(t.name, "refus.tsv")
        os.makedirs(os.path.join(self.t, "faux"))
        with open(os.path.join(self.t, "faux", "date"), "w", encoding="utf-8") as f:
            f.write("#!/bin/sh" + NL + "echo " + H + NL)
        os.chmod(os.path.join(self.t, "faux", "date"), 0o755)
        self.env = dict(os.environ, SHOGEN_GARDE_REFUS=self.j, PATH=os.path.join(self.t, "faux") + os.pathsep
                        + os.environ["PATH"])

    def lancer(self, ev, avant=(), **plus):
        tp = os.path.join(self.t, "journal.txt")
        with open(tp, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(e) + NL for e in avant)
        e = {"hook_event_name": ev, "transcript_path": tp, "cwd": self.t, **plus}
        p = subprocess.run([sys.executable, "-I", GARDE], input=json.dumps(e), capture_output=True, text=True,
                           timeout=60, env=self.env)
        return p.returncode, p.stdout

    def lire(self):
        with open(self.j, encoding="utf-8") as f:
            return f.read()


class Journal(Base):
    """Le crochet : lignes du journal, en-tête."""
    def test_refus_journal_des_passages(self):
        """Passage (permis), refus R7 et R6 (règle), sous-agent (agent), erreur interne (erreur), acte d'un secret et
        d'une valeur après tabulation (masqués, abrégé à 80) : une ligne chacun, en-tête une fois ; dossier du journal absent : rien."""
        secret = ("echo " + chr(34) + "token=s3cr3tValeur" + chr(34) + " sk-ant-" + "api03-AbCdEf0123456789xyzXYZ0" + TAB
                  + "password:" + TAB + "motdepasse" + TAB)
        texte = {"type": "assistant", "uuid": "u1", "message": {"content": [{"type": "text", "text": "Il y a 4321 cas."}]}}
        codes = [self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": "ls"})[0],
                 self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": "sleep 5"})[0],
                 self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": secret + "x" * 99})[0],
                 self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": "ls"}, agent_id="a1")[0],
                 self.lancer("Stop", [texte])[0], self.lancer("PreToolUse", tool_name="Bash", tool_input=["x"])[0]]
        abrege = "echo " + chr(34) + "token=***" + chr(34) + " *** password: *** "
        lignes = [["PreToolUse:Bash", "permis", "ls", "principal"], ["PreToolUse:Bash", "R7", "sleep 5", "principal"],
                  ["PreToolUse:Bash", "permis", abrege + "x" * (80 - len(abrege)), "principal"],
                  ["PreToolUse:Bash", "permis", "ls", "a1"], ["Stop", "R6", "-", "principal"],
                  ["PreToolUse:Bash", "erreur", "-", "principal"]]
        self.assertEqual((codes, self.lire()), ([0, 2, 0, 0, 2, 0], ENTETE + "".join(TAB.join([H, *x]) + NL
                                                                                    for x in lignes)))
        self.assertNotIn("motdepasse", self.lire())
        self.env["SHOGEN_GARDE_REFUS"] = os.path.join(self.t, "absent", "refus.tsv")
        self.assertEqual(self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": "sleep 5"})[0], 2)
        self.assertEqual(sorted(os.listdir(self.t)), ["faux", "garde-faits.etat", "garde-faits.log", "journal.txt",
                                                      "refus.tsv"])

    def test_refus_entete_unique(self):
        """Journal créé entre le test d'existence et la pose de l'en-tête (crochets concurrents) : ni second en-tête, ni
        ligne perdue, ni fichier temporaire laissé ; journal absent : en-tête puis ligne."""
        spec = importlib.util.spec_from_file_location("garde_faits_refus", GARDE)
        g = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(g)
        with open(self.j, "w", encoding="utf-8") as f:
            f.write(ENTETE + "avant" + NL)
        with mock.patch.dict(os.environ, self.env), mock.patch.object(g.os.path, "exists", return_value=False):
            g.consigner({"hook_event_name": "Stop"}, "R6")
        self.assertEqual((self.lire(), sorted(os.listdir(self.t))), (ENTETE + "avant" + NL + TAB.join(
            [H, "Stop", "R6", "-", "principal"]) + NL, ["faux", "refus.tsv"]))
        os.remove(self.j)
        with mock.patch.dict(os.environ, self.env):
            g.consigner({"hook_event_name": "Stop"}, "permis")
        self.assertEqual(self.lire(), ENTETE + TAB.join([H, "Stop", "permis", "-", "principal"]) + NL)
