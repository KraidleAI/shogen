"""Cas de avant_acte.py (lot GARDE-FOUS-ORCH), dans des dépôts git temporaires isolés (tests/aide_garde.py), jamais le
dépôt du projet ; rouges sur l'erreur réelle reproduite, verts sur le cas sain. GF-5 : sceller (LA-N05 : pièce
retouchée après la vérification, commit sans verdict vert sur le contenu exact), contrat de sortie, journal.
GF-5b : commit C1 (sceau), C2 (Source-Sha ; E8 : message écrit avant la clôture de la source), C3 (E8 : « trois
passes » contre deux ; verdicts, identifiants et sha courts lus dans les sources ou résolus par git).
GF-6 : commit C4 (E14, heures), C5 (E16, citations), C6 (LA-N04, index égal aux diffs nommés), C7 (E21, aucun bloc
qui décale une ligne d'un fichier cité par numéro), C9 (Diff-Id)."""
import contextlib
import hashlib
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import avant_acte
from tests import aide_garde as ag

NL = chr(10)
ADJ = ("Contre-contrôle CONFORME en deux passes ; "
       "G2 ACCEPTE-AVEC-CORRECTIONS, G-1 à G-5 ; SHOGEN-FUZZ-DISTILLATION-1." + NL)


class Depot(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.tmp = t.name
        self.d, self.env = ag.depot(self.tmp, {"a.md": "un" + NL})
        env = mock.patch.dict(os.environ, self.env, clear=True)
        env.start()
        self.addCleanup(env.stop)

    def lancer(self, *argv, depot=None):
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(io.StringIO()):
            code = avant_acte.main(["--depot", depot or self.d, *argv])
        return code, sortie.getvalue()

    def indexer(self, fichiers):
        ag.ecrire(self.d, fichiers)
        ag.git(self.d, self.env, "add", "-A")

    def journal(self):
        with open(os.path.join(self.d, ".git", "shogen-garde", "journal.tsv"), encoding="utf-8") as f:
            return [x.split(chr(9)) for x in f.read().splitlines()]


class Sceau(Depot):
    def test_la_n05_sceau_du_contenu_verifie(self):
        """LA-N05 : pas de sceau sur un fichier non suivi ni sur une modification hors de l'index ; sceau posé sous la
        clé de la tête et de l'arbre indexé ; --tete exige l'index égal à HEAD."""
        ag.ecrire(self.d, {"b.md": "x"})
        self.assertEqual(self.lancer("sceller")[0], 1)
        os.remove(os.path.join(self.d, "b.md"))
        ag.ecrire(self.d, {"a.md": "modifié" + NL})
        code, sortie = self.lancer("sceller")
        self.assertEqual((code, sortie[:9]), (1, "REFUS S1 "))
        ag.git(self.d, self.env, "add", "-A")
        self.assertEqual([self.lancer("sceller")[0], self.lancer("sceller", "--tete")[0]], [0, 1])
        sceaux = os.listdir(os.path.join(self.d, ".git", "shogen-garde", "sceaux"))
        self.assertEqual(sceaux, [avant_acte.cle(self.d)])

    def test_cle_de_la_tete_et_de_l_index(self):
        """Pièce retouchée après le sceau : autre clé ; même arbre sous une autre tête : autre clé ; --tete à part."""
        cles = [avant_acte.cle(self.d), avant_acte.cle(self.d, tete=True)]
        self.indexer({"a.md": "un retouché" + NL})
        cles.append(avant_acte.cle(self.d))
        tete = ag.git(self.d, self.env, "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "autre").strip()
        ag.git(self.d, self.env, "update-ref", "HEAD", tete)
        cles += [avant_acte.cle(self.d), avant_acte.cle(self.d, tete=True)]
        self.assertEqual(len(set(cles)), 5)

    def test_contrat_et_journal(self):
        """Sorties 0, 1, 3 (sous-commande inconnue, dépôt absent) ; journal : heure de date -u, sous-commande, code,
        niveau, contourne ; une ligne par refus, une ligne conforme sinon ; outil lancé sous -I."""
        self.assertEqual(self.lancer("inconnue")[0], 3)
        self.assertEqual(self.lancer("sceller", depot=os.path.join(self.tmp, "absent"))[0], 3)
        ag.ecrire(self.d, {"b.md": "x"})
        self.assertEqual(self.lancer("sceller")[0], 1)
        os.remove(os.path.join(self.d, "b.md"))
        p = subprocess.run([sys.executable, "-I", "-B", avant_acte.__file__, "--depot", self.d, "sceller"],
                           capture_output=True, text=True, env=self.env, timeout=120)
        self.assertEqual((p.returncode, p.stdout), (0, ""), p.stderr)
        j = self.journal()
        self.assertEqual([x[1:] for x in j], [["sceller", "S1", "refus", "-"], ["sceller", "-", "conforme", "-"]])
        self.assertTrue(all(re.fullmatch("20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", x[0]) for x in j))


class Source(Depot):
    def setUp(self):
        super().setUp()
        self.adj = os.path.join(self.tmp, "ADJUDICATION.md")
        ag.ecrire(self.tmp, {"ADJUDICATION.md": ADJ})
        self.indexer({"a.md": "un" + NL + "deux" + NL})

    def message(self, corps, source=None):
        """Message écrit depuis la source : une ligne Source-Sha à son sha256 du moment."""
        with open(source or self.adj, "rb") as f:
            ag.ecrire(self.tmp, {"m.txt": corps + NL + NL + "Source-Sha: " + hashlib.sha256(f.read()).hexdigest() + NL})
        return os.path.join(self.tmp, "m.txt")

    def commit(self, m):
        return self.lancer("commit", "--message", m, "--source", self.adj)


class Commit(Source):
    def test_la_n05_commit_sans_sceau(self):
        """LA-N05, C1 : commit sans sceau refusé ; vérification puis sceau : admis ; pièce retouchée après : refusé."""
        m = self.message("x : contre-contrôle CONFORME en deux passes")
        code, sortie = self.commit(m)
        self.assertEqual((code, sortie[:9]), (1, "REFUS C1 "))
        self.assertEqual(self.lancer("sceller")[0], 0)
        self.assertEqual(self.commit(m), (0, ""))
        self.indexer({"a.md": "un" + NL + "deux retouché" + NL})
        self.assertEqual(self.commit(m)[0], 1)

    def test_e8_source_sha(self):
        """E8, C2 : message écrit avant la clôture (source retouchée ensuite) : refus, pour la source sans ligne et pour
        la ligne périmée ; message sans Source-Sha : refus ; réécrit depuis la source finale : admis ; source sous un
        interdit : erreur, jamais lue."""
        self.lancer("sceller")
        m = self.message("x : contre-contrôle CONFORME en deux passes")
        ag.ecrire(self.tmp, {"ADJUDICATION.md": ADJ + "Clôture du contre-contrôle." + NL})
        code, sortie = self.commit(m)
        self.assertEqual((code, sortie.count("REFUS C2 ")), (1, 2))
        ag.ecrire(self.tmp, {"n.txt": "x : contre-contrôle CONFORME en deux passes" + NL})
        self.assertEqual(self.commit(os.path.join(self.tmp, "n.txt"))[0], 1)
        self.assertEqual(self.commit(self.message("x : contre-contrôle CONFORME en deux passes")), (0, ""))
        ag.ecrire(self.tmp, {"docs/rapports/a.md": ADJ})
        interdit = os.path.join(self.tmp, "docs", "rapports", "a.md")
        self.assertEqual(self.lancer("commit", "--message", m, "--source", interdit)[0], 3)

    def test_e8_mots_du_message(self):
        """E8, C3 : CONFORME en trois passes contre deux passes : refus ; verdict, identifiant ou sha court absents
        des sources et inconnus de git, verdict lu seulement dans un mot plus long : refus ; pieds (Diff-Id,
        Co-Authored-By) non lus ; nombre en lettres capitales ramené en chiffres."""
        self.lancer("sceller")
        for corps in ["FUZZ FZ-g : contre-controle CONFORME en trois passes", "x : NON-CONFORME", "x : ACCEPTE",
                      "x : SHOGEN-INCONNU-1", "x : C-7", "x : commit 1234abc"]:
            code, sortie = self.commit(self.message(corps))
            self.assertEqual((code, sortie[:9]), (1, "REFUS C3 "), corps)
        ag.ecrire(self.tmp, {"ADJUDICATION.md": "Verdict : NONCONFORME, en deux passes." + NL})
        self.assertEqual(self.commit(self.message("x : CONFORME en deux passes"))[1][:9], "REFUS C3 ")
        ag.ecrire(self.tmp, {"ADJUDICATION.md": ADJ})
        tete = ag.git(self.d, self.env, "rev-parse", "HEAD").strip()
        corps = NL.join(["FUZZ FZ-g : G2 ACCEPTE-AVEC-CORRECTIONS G-1 a G-5, contre-controle CONFORME en deux passes",
                         "base " + tete[:9] + ", SHOGEN-FUZZ-DISTILLATION-1 ; Deux passes", "", "Diff-Id: R-9",
                         "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"])
        self.assertEqual(self.commit(self.message(corps)), (0, ""))



class CommitSuite(Source):
    CORPS = "x : contre-contrôle CONFORME en deux passes"

    def verifier(self, fichiers, corps=CORPS, *argv):
        """Indexe `fichiers`, scelle, puis lance commit avec un message écrit depuis la source."""
        self.indexer(fichiers)
        self.lancer("sceller")
        return self.lancer("commit", "--message", self.message(corps), "--source", self.adj, *argv)

    def test_e14_e16_lignes_ajoutees(self):
        """E14 (04:22 écrit à 04:14) dans une ligne ajoutée d'un .md, non d'un .py, et dans le message : refus C4 ;
        E16, citation stricte inexacte ajoutée : refus C5 ; forme libre : avertissement, sortie 0, journal ; fichier
        indexé sous un interdit : jamais lu, avertissement."""
        faux = os.path.join(self.tmp, "faux")
        ag.ecrire(faux, {"date": "#!/bin/sh" + NL + "echo 2026-10-10T04:14:00Z" + NL})
        os.chmod(os.path.join(faux, "date"), 0o755)
        os.environ["PATH"] = faux + os.pathsep + os.environ["PATH"]
        code, sortie = self.verifier({"a.md": "un" + NL + "page du 2026-10-10 04:22" + NL, "c.py": "2026-10-10 04:22",
                                      "docs/rapports/r.md": "2026-10-10 04:22"})
        self.assertEqual((code, sortie.count("REFUS C4 ")), (1, 1))
        self.assertIn("REFUS C4 : heure-future à a.md:2 : 2026-10-10 04:22", sortie)
        self.assertIn("AVERTISSEMENT C4 : 1 fichier(s) indexé(s) sous un interdit, non lus", sortie)
        ag.git(self.d, self.env, "rm", "-q", "-f", "docs/rapports/r.md")
        code, sortie = self.verifier({"a.md": "un" + NL, "b.md": "b"}, "x : CONFORME en deux passes, 2026-10-10 04:22")
        self.assertEqual((code, sortie[:9]), (1, "REFUS C4 "))
        cit = chr(171) + " Q-FUZZ-1 routée vers les advisors " + chr(187)
        code, sortie = self.verifier({"c.md": cit + " (a.md:1)" + NL})
        self.assertEqual((code, sortie[:9]), (1, "REFUS C5 "))
        code, sortie = self.verifier({"c.md": "x" + NL + cit + " (JOURNAL l.1)" + NL})
        self.assertEqual((code, sortie.startswith("AVERTISSEMENT C5 : citation-libre")), (0, True))
        self.assertEqual(self.journal()[-1][1:], ["commit", "C5", "avertissement", "-"])

    def test_la_n04_diffs_nommes(self):
        """LA-N04 : deux diffs indexés, un seul nommé : refus C6 ; les deux nommés, dans l'ordre : admis."""
        self.indexer({"a.md": "un" + NL + "deux" + NL, "z.md": "z" + NL})
        diffs = []
        for nom in ("a.md", "z.md"):
            ag.ecrire(self.tmp, {nom + ".diff": ag.git(self.d, self.env, "diff", "--cached", "HEAD", "--", nom)})
            diffs.append(os.path.join(self.tmp, nom + ".diff"))
        self.assertEqual(self.verifier({}, self.CORPS, "--diff", diffs[1])[1][:9], "REFUS C6 ")
        self.assertEqual(self.verifier({}, self.CORPS, "--diff", diffs[0], "--diff", diffs[1]), (0, ""))

    def test_e21_fichier_cite(self):
        """E21 : insertion au milieu d'un fichier cité par numéro (JOURNAL.md) : refus C7 ; remplacement à nombre de
        lignes égal et ajout en fin : admis ; décalage écrit dans le message : admis, journal contourne."""
        self.indexer({"JOURNAL.md": NL.join(["l1", "l2", "l3", ""])})
        ag.git(self.d, self.env, "commit", "-q", "-m", "journal")
        code, sortie = self.verifier({"JOURNAL.md": NL.join(["l1", "neuf", "l2", "l3", ""])})
        self.assertEqual((code, sortie[:9]), (1, "REFUS C7 "))
        self.assertEqual(self.verifier({"JOURNAL.md": NL.join(["l1", "L2", "l3", "fin", ""])}), (0, ""))
        code, sortie = self.verifier({"JOURNAL.md": NL.join(["l1", "neuf", "L2", "l3", "fin", ""])},
                                     self.CORPS + NL + NL + "Décalage admis : JOURNAL.md")
        self.assertEqual((code, sortie[:9]), (0, "ADMIS C7 "))
        self.assertEqual(self.journal()[-1][1:], ["commit", "C7", "admis", "decalage-admis"])

    def test_diff_id(self):
        """C9 : ligne Diff-Id exigée quand --id est donné."""
        self.assertEqual(self.verifier({"a.md": "id" + NL}, self.CORPS, "--id", "GF-6")[1][:9], "REFUS C9 ")
        self.assertEqual(self.verifier({}, self.CORPS + NL + NL + "Diff-Id: GF-6", "--id", "GF-6"), (0, ""))
