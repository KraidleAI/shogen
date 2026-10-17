"""Cas du journal des refus du crochet GARDE-FAITS (GARDE-FOUS phase 3, annexe B, B.108 : phase 3 de
SHOGEN-GARDE-FOUS-ORCH-1) : une ligne par refus et par passage, acte abrégé sans secret, en-tête unique. Le crochet du
dépôt est lancé tel quel sur des journaux synthétiques (nom en .txt), son journal des refus dans un dossier temporaire
(SHOGEN_GARDE_REFUS), l'heure fixée par un faux date en tête du PATH.
Relevé des refus au premier message d'une session (classe Journal).
Lecteur du journal : avant_acte.py refus (classe Lecteur)."""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import avant_acte

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GARDE = os.path.join(RACINE, ".claude", "hooks", "garde_faits.py")
NL, TAB = chr(10), chr(9)
H = "2026-10-16T10:00:00Z"
ENTETE = TAB.join(["heure", "evenement", "regle", "acte", "agent"]) + NL
RELEVE = "RELEVÉ DES REFUS (crochet du dépôt, phase 3) : "
DETAIL = " ; détail : python3 -I -B scripts/controle/avant_acte.py refus"


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
    """Le crochet : lignes du journal, en-tête, relevé au premier message."""
    def test_refus_journal_des_passages(self):
        """Passage (permis), refus R7 et R6 (règle), sous-agent (agent), erreur interne (erreur), acte d'un secret et
        d'une valeur après tabulation (masqués, abrégé à 80) : une ligne chacun, en-tête une fois ; dossier du journal absent : rien.
        G2, C-4 : refus R11 (consigne longue sans brief) et R10 (dossier nommé sans relevé) consignés sous leur règle.
        Intégration P3 (SHOGEN-GARDE-ERREUR-INTERNE-1) : erreur interne ou journal illisible sur un acte qui écrit :
        refus consigné R0 ; erreur interne ou journal illisible sur une lecture pure : permis, consigné erreur (CC
        de l'intégration P3, R-1 ; le sous-agent a1 n'a pas de journal ici). Refus R12 (nombre à unité
        sans pièce, R6 couverte par un 28 affiché sans unité) : consigné R12."""
        secret = ("echo " + chr(34) + "token=s3cr3tValeur" + chr(34) + " sk-ant-" + "api03-AbCdEf0123456789xyzXYZ0" + TAB
                  + "password:" + TAB + "motdepasse" + TAB)
        texte = {"type": "assistant", "uuid": "u1", "message": {"content": [{"type": "text", "text": "Il y a 4321 cas."}]}}
        codes = [self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": "ls"})[0],
                 self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": "sleep 5"})[0],
                 self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": secret + "x" * 99})[0],
                 self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": "ls"}, agent_id="a1")[0],
                 self.lancer("Stop", [texte])[0], self.lancer("PreToolUse", tool_name="Bash", tool_input=["x"])[0],
                 self.lancer("PreToolUse", [{"type": "assistant", "message": "x"}], tool_name="Bash",
                             tool_input={"command": "ls"})[0],
                 self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": "git commit -m x"},
                             transcript_path=os.path.join(self.t, "absent.txt"))[0],
                 self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": "ls"},
                             transcript_path=os.path.join(self.t, "absent.txt"))[0],
                 self.lancer("PreToolUse", tool_name="Agent", tool_input={"prompt": "x" * 1600})[0],
                 self.lancer("Stop", [{"type": "user", "message": {"content": "Note de Zorglubien."}}, {
                     "type": "assistant", "uuid": "u2", "message": {"content": [{"type": "text", "text": "Voir MONARK."}]}}])[0],
                 self.lancer("Stop", [{"type": "user", "message": {"content": "Quelle durée ?"}}, {
                     "type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t1", "name": "Bash", "input": {
                         "command": "grep -n collecte notes.txt"}}]}}, {"type": "user", "message": {"content": [{
                             "type": "tool_result", "tool_use_id": "t1", "content": "28:collecte"}]}}, {
                     "type": "assistant", "uuid": "u3", "message": {"content": [{"type": "text", "text": "Pendant les 28 "
                                                                                 "jours de collecte."}]}}])[0]]
        abrege = "echo " + chr(34) + "token=***" + chr(34) + " *** password: *** "
        lignes = [["PreToolUse:Bash", "permis", "ls", "principal"], ["PreToolUse:Bash", "R7", "sleep 5", "principal"],
                  ["PreToolUse:Bash", "permis", abrege + "x" * (80 - len(abrege)), "principal"],
                  ["PreToolUse:Bash", "erreur", "ls", "a1"], ["Stop", "R6", "-", "principal"],
                  ["PreToolUse:Bash", "R0", "-", "principal"], ["PreToolUse:Bash", "erreur", "ls", "principal"],
                  ["PreToolUse:Bash", "R0", "git commit -m x", "principal"], ["PreToolUse:Bash", "erreur", "ls", "principal"],
                  ["PreToolUse:Agent", "R11", '{"prompt": "' + "x" * 68, "principal"], ["Stop", "R10", "-", "principal"],
                  ["Stop", "R12", "-", "principal"]]
        self.assertEqual((codes, self.lire()), ([0, 2, 0, 0, 2, 2, 0, 2, 0, 2, 2, 2], ENTETE + "".join(TAB.join([H, *x]) + NL
                                                                                    for x in lignes)))
        self.assertNotIn("motdepasse", self.lire())
        self.env["SHOGEN_GARDE_REFUS"] = os.path.join(self.t, "absent", "refus.tsv")
        self.assertEqual(self.lancer("PreToolUse", tool_name="Bash", tool_input={"command": "sleep 5"})[0], 2)
        self.assertEqual(sorted(os.listdir(self.t)), ["faux", "garde-faits.etat", "garde-faits.log", "journal.txt",
                                                      "refus.tsv"])

    def test_refus_entete_unique(self):
        """Journal créé entre le test d'existence et la pose de l'en-tête (crochets concurrents) : ni second en-tête, ni
        ligne perdue, ni fichier temporaire laissé ; journal absent : en-tête puis ligne. G2, C-2 : abreger masque le mot
        de passe d'une URL et de curl -u, garde le port d'une URL."""
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
        self.assertEqual([g.abreger(x) for x in ("git clone https://alice:Motdepasse2026@forge.example.org/r.git",
                                                 "curl -u alice:hunter2hunter2 https://h", "curl https://h:8080/x")],
                         ["git clone https://alice:***@forge.example.org/r.git", "curl -u alice:*** https://h",
                          "curl https://h:8080/x"])

    def test_refus_releve_premier_message(self):
        """Premier message d'une session (journal de session vide, ou ne portant que ce message) : refus depuis la
        dernière ligne releve, par règle (plus fréquente d'abord), ligne releve écrite ; message suivant : rien ; aucun
        relevé d'avant : depuis le début ; noms propres : relevé E26 d'abord, refus en dernier. G2, C-3 : autre message
        en tête d'un journal de session de plus de QUEUE octets : rien ; entrée illisible : relevé E26 gardé ; journal
        des refus non écrit : dit, non « 0 refus »."""
        avant = [["2026-10-14T08:00:00Z", "PreToolUse:Bash", "R5", "git commit", "principal"],
                 ["2026-10-15T09:00:00Z", "UserPromptSubmit", "releve", "1 refus", "principal"],
                 ["2026-10-15T10:00:00Z", "PreToolUse:Bash", "R7", "sleep 5", "principal"],
                 ["2026-10-15T11:00:00Z", "PreToolUse:Bash", "R2", "sed -i x f", "a1"],
                 ["2026-10-15T12:00:00Z", "PreToolUse:Bash", "R7", "sleep 9", "principal"],
                 ["2026-10-15T12:30:00Z", "PreToolUse:Bash", "R0", "git commit", "principal"],
                 ["2026-10-15T13:00:00Z", "PreToolUse:Bash", "permis", "ls", "principal"]]
        with open(self.j, "w", encoding="utf-8") as f:
            f.write(ENTETE + "".join(TAB.join(x) + NL for x in avant) + "ligne illisible" + NL)
        q = "où en est la suite ?"
        self.assertEqual(self.lancer("UserPromptSubmit", prompt=q), (0, RELEVE + "4 refus depuis le dernier relevé "
                         "(2026-10-15T09:00:00Z) : R7 ×2, R0 ×1, R2 ×1" + DETAIL + " --depuis 2026-10-15" + NL))
        fin = [TAB.join([H, "UserPromptSubmit", "releve", "4 refus", "principal"]) + NL,
               TAB.join([H, "UserPromptSubmit", "permis", "-", "principal"]) + NL]
        self.assertEqual(self.lire().split(NL)[-3:], [x[:-1] for x in fin] + [""])
        humain = {"type": "user", "message": {"role": "user", "content": "Bonjour."}}
        self.assertEqual(self.lancer("UserPromptSubmit", [humain], prompt=q), (0, ""))
        meme = {"type": "user", "message": {"role": "user", "content": q}}
        self.assertEqual(self.lancer("UserPromptSubmit", [meme], prompt=q), (0, RELEVE + "0 refus depuis le dernier "
                         "relevé (" + H + ")" + DETAIL + " --depuis 2026-10-16" + NL))
        with open(self.j, "w", encoding="utf-8") as f:
            f.write(ENTETE + TAB.join(avant[0]) + NL)
        code, sortie = self.lancer("UserPromptSubmit", prompt="Note de Zorglubien sur la suite.")
        self.assertEqual((code, sortie.split(NL)[0][:31], sortie.split(NL)[-2]),
                         (0, "RELEVÉ (crochet du dépôt, E26) ", RELEVE + "1 refus depuis le début du journal : R5 ×1"
                          + DETAIL))
        long = {"type": "assistant", "message": {"content": [{"type": "text", "text": "x" * 6_000_001}]}}
        self.assertEqual(self.lancer("UserPromptSubmit", [humain, long], prompt=q), (0, ""))
        chaine = {"type": "user", "message": "texte en chaîne"}
        code, sortie = self.lancer("UserPromptSubmit", [chaine], prompt="Note de Zorglubien sur la suite.")
        self.assertEqual((code, sortie.split(NL)[0][:31], RELEVE in sortie), (0, "RELEVÉ (crochet du dépôt, E26) ", False))
        self.env["SHOGEN_GARDE_REFUS"] = absent = os.path.join(self.t, "absent", "refus.tsv")
        self.assertEqual(self.lancer("UserPromptSubmit", prompt=q), (0, RELEVE + "journal " + absent
                                                                     + " absent ou non écrit : aucun refus relevé" + NL))


class Lecteur(Base):
    """avant_acte.py refus : relevé du journal des refus (heure du jour fixée à H)."""
    def releve(self, *argv):
        sortie = io.StringIO()
        with mock.patch.dict(os.environ, self.env), contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(
                io.StringIO()):
            code = avant_acte.main(["--depot", self.t, "refus", *argv])
        return code, sortie.getvalue().split(NL)[:-1]

    def test_refus_lecteur(self):
        """Refus par règle et par jour (numéro de règle croissant), dix actes au plus (plus fréquent, puis ordre des
        textes, non ordre du journal ; règles jointes par numéro), règles du crochet sans refus depuis trente jours (borne comprise, tout le journal),
        passages (permis, erreur ; releve exclu), lignes illisibles, --depuis ; date fausse, journal absent : 3."""
        b = "PreToolUse:Bash"
        lignes = [["2026-09-15T08:00:00Z", b, "R1", "rm -rf w"], ["2026-09-16T08:00:00Z", "Stop", "R6", "-"],
                  ["2026-09-30T08:00:00Z", b, "permis", "ls"]]
        lignes += [[f"2026-10-15T0{k}:00:00Z", b, "R5", "git commit -m x"] for k in (1, 2, 3)]
        lignes += [["2026-10-16T02:30:00Z", b, "R0", "git commit -m x"]]      # marque R0 (CC de l'intégration P3, R-3)
        lignes += [["2026-10-16T03:00:00Z", b, "R7", "sleep 5"], ["2026-10-16T04:00:00Z", "PreToolUse:Agent", "R11",
                                                                  "sleep 5"]]
        lignes += [[f"2026-10-16T0{k}:00:00Z", b, "R2", "sed -i s f"] for k in (1, 2)]
        lignes += [[f"2026-10-16T1{k}:00:00Z", "PreToolUse:Agent", "R11", f"acte-0{k}"] for k in range(9, 0, -1)]
        lignes += [["2026-10-16T05:00:00Z", "UserPromptSubmit", "releve", "3 refus"]]
        lignes += [["2026-10-16T06:00:00Z", b, "permis", "ls"]] * 2 + [["2026-10-16T07:00:00Z", b, "erreur", "-"]]
        os.makedirs(os.path.join(self.t, "scripts", "controle", "garde"))
        with open(os.path.join(self.t, "scripts", "controle", "garde", "refus.tsv"), "w", encoding="utf-8") as f:
            f.write(ENTETE + "".join(TAB.join([*x, "principal"]) + NL for x in lignes) + "x" + NL
                    + TAB.join(["2026-10-16T08:00:00Z", "Stop", "R6", "-"]) + NL)
        self.assertEqual(self.releve("--depuis", "2026-10-01"), (0, [
            "journal des refus : 24 ligne(s) lue(s), 2 illisible(s) ; depuis 2026-10-01 : 17 refus",
            "refus par règle et par jour :", "  2026-10-15" + TAB + "R5" + TAB + "3", "  2026-10-16" + TAB + "R0" + TAB + "1",
            "  2026-10-16" + TAB + "R2" + TAB
            + "2", "  2026-10-16" + TAB + "R7" + TAB + "1", "  2026-10-16" + TAB + "R11" + TAB + "10",
            "actes refusés les plus fréquents (dix au plus) :",
            "  4" + TAB + "R0,R5" + TAB + "git commit -m x", "  2" + TAB + "R2" + TAB + "sed -i s f",
            "  2" + TAB + "R7,R11" + TAB + "sleep 5"] + ["  1" + TAB + "R11" + TAB + f"acte-0{k}" for k in range(1, 8)] + [
            "règles sans refus depuis trente jours (depuis le 2026-09-16, candidates à relire) : R1, R3, R4, R8, R9, R10, R12, R13",
            "passages : 3 (dont 1 erreur(s) interne(s), acte permis sans contrôle)"]))
        self.assertEqual(self.releve()[1][0], "journal des refus : 24 ligne(s) lue(s), 2 illisible(s) ; depuis le "
                         "début : 19 refus")
        self.assertEqual((self.releve("--depuis", "2026-10-1")[0], self.releve("--journal", self.j)[0]), (3, 3))
