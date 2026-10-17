"""Cas de SHOGEN-GARDE-ERREUR-INTERNE-1 (GARDE-FOUS phase 3, groupe B ; annexe B, B.109 ; G2 du correctif CQ-1, C-1) :
une erreur interne du crochet GARDE-FAITS, ou un journal illisible, pendant le jugement d'un acte qui écrit, commet,
pousse, supprime ou crée une PR (R1 à R3, R5, R8) est un refus ; un acte de lecture pure reste permis, l'erreur écrite.
L'erreur est provoquée par un double (mock) ; le crochet est chargé par son chemin et joué en processus, sur un journal
synthétique (nom en .txt) d'un dossier temporaire."""
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
REEL = "curl 'http://[' ; git commit -m essai"        # cas réel de la G2 (preuves/08 de revue-codeql-pr12)


def charger():
    spec = importlib.util.spec_from_file_location("garde_faits_ei", GARDE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ErreurInterne(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.t, self.g = t.name, charger()
        self.journal = os.path.join(self.t, "journal.txt")
        lu = [{"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t1", "name": "Bash",
                                                              "input": {"command": "git status --short"}}]}},
              {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "content": ""}]}}]
        with open(self.journal, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(e) + NL for e in lu)

    def jouer(self, nom, inp, journal=None):
        """(sortie, stderr) du crochet sur un PreToolUse ; un refus par sys.exit(2) compte comme sortie 2."""
        e = {"hook_event_name": "PreToolUse", "transcript_path": journal or self.journal, "cwd": self.t,
             "tool_name": nom, "tool_input": inp}
        err = io.StringIO()
        with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(e))), contextlib.redirect_stderr(err):
            try:
                code = self.g.main()
            except SystemExit as x:
                code = x.code
        return code, err.getvalue()

    def test_cas_reel_de_la_g2_refuse(self):
        """C-1 de la G2 CQ-1 : sous l'ancien crochet, une ValueError levée en lisant curl 'http://[' faisait sortir 0
        (acte permis sans contrôle) et sauter R3 sur le git commit de la même commande ; erreur provoquée ici par un
        double de hote_forge : refus (sortie 2), message d'erreur nommé, refus écrit au journal des décisions."""
        with mock.patch.object(self.g, "hote_forge", side_effect=ValueError("Invalid IPv6 URL")):
            code, err = self.jouer("Bash", {"command": REEL})
        self.assertEqual((code, "REFUS" in err, "ValueError('Invalid IPv6 URL')" in err), (2, True, True), err)
        with open(os.path.join(self.t, "garde-faits.log"), encoding="utf-8") as f:
            self.assertIn("REFUS", f.read())

    def test_table_des_cas(self):
        """Table du README : erreur interne (double de faits_et_appels) ; actes qui écrivent, commettent, poussent,
        suppriment, lancent un agent ou créent une PR : refus ; lectures pures (programmes de lecture, git en lecture,
        outils mcp de lecture de la forge) : permises, erreur écrite."""
        refus = [("Bash", {"command": c}) for c in (
            "git commit -m essai", "git push origin main", "rm -rf clone", "cat a > b", "echo x | tee b",
            "sed -n 1p a", "git log --output=f", "GIT_PAGER=rm git log", "cat $(ls)", "echo x | sh", "git -c a=b log",
            "git status $X", "grep 'a|b' f", "ls ; curl https://api.github.com/x", "cat a >> b", "cd x && make", "F=/bin/cat rm -rf y")] + [
            ("Write", {"file_path": "/x/a.md", "content": "x"}), ("Edit", {"file_path": "/x/a.md"}),
            ("Agent", {"prompt": "x"}), ("mcp__github__create_pull_request", {"owner": "o", "repo": "r"}),
            ("mcp__github__merge_pull_request", {}), ("Inconnu", {})]
        permis = [("Bash", {"command": c}) for c in (
            "cat NOTES.md", "grep -n x f | wc -l", "git status --short", "git -C /x log --oneline -3",
            "ls -la 2>/dev/null", "head -3 a 2>&1 | tail -1", "sha256sum a b", "git --no-pager diff --stat -- a",
            "cd /x && ls")] + [("mcp__github__list_commits", {}), ("mcp__github__get_me", {})]
        with mock.patch.object(self.g, "faits_et_appels", side_effect=RuntimeError("double")):
            vus = {(n, json.dumps(i)): self.jouer(n, i) for n, i in refus + permis}
        for n, i in refus:
            code, err = vus[(n, json.dumps(i))]
            self.assertEqual((code, "erreur interne" in err), (2, True), (n, i, err))
        for n, i in permis:
            code, err = vus[(n, json.dumps(i))]
            self.assertEqual((code, "erreur interne" in err, "REFUS" in err), (0, True, False), (n, i, err))

    def test_journal_illisible(self):
        """L.610 : journal illisible (absent) ; acte qui commet : refus ; lecture pure : permise, note écrite."""
        absent = os.path.join(self.t, "absent.txt")
        code, err = self.jouer("Bash", {"command": "git commit -m essai"}, journal=absent)
        self.assertEqual((code, "journal illisible" in err, "REFUS" in err), (2, True, True), err)
        code, err = self.jouer("Bash", {"command": "cat NOTES.md"}, journal=absent)
        self.assertEqual((code, "journal illisible" in err, "REFUS" in err), (0, True, False), err)


if __name__ == "__main__":
    unittest.main()
