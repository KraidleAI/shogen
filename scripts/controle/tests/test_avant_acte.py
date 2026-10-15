"""Cas de avant_acte.py (lot GARDE-FOUS-ORCH), dans des dépôts git temporaires isolés (tests/aide_garde.py), jamais le
dépôt du projet ; rouges sur l'erreur réelle reproduite, verts sur le cas sain. GF-5 : sceller (LA-N05 : pièce
retouchée après la vérification, commit sans verdict vert sur le contenu exact), contrat de sortie, journal.
GF-5b : commit C1 (sceau), C2 (Source-Sha ; E8 : message écrit avant la clôture de la source), C3 (E8 : « trois
passes » contre deux ; verdicts, identifiants et sha courts lus dans les sources ou résolus par git).
GF-6 : commit C4 (E14, heures), C5 (E16, citations), C6 (LA-N04, index égal aux diffs nommés), C7 (E21, aucun bloc
qui décale une ligne d'un fichier cité par numéro), C9 (Diff-Id).
GF-6b : C8 (E1, workflows lus en YAML) ; diff d'un worker reçu avant la G2 : E21, E14, E16, E9 (presg5), E1,
interdits, diff qui ne s'applique pas sur la tête.
GF-7 : verser (E9 : messages d'outils anglais entre guillemets, S-G5 ; E10 : adjudication versée en double).
GF-8 : pousser (LA-N05 : poussée rouge ; ADR-0028 l.293 : docs 15/16 jamais au distant ; E17 : actes que le
mandataire refuse) et publier (E14 : heure future dans un texte publié ; secret ; chemin du scratchpad).
GF-8b : existe (E15 : absence affirmée sans recherche du nom) et disque (E4 : disque presque plein, cibles cargo).
GF-9b : chaine (E11 : chaîne lancée avec un diff rouge seul, que le tableau du contre-contrôle annonçait ; E25 :
chaîne de 23 commits, environ 126 min, lancée en tâche liée sous la borne de 120 min)."""
import contextlib
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import collections
import unittest
from unittest import mock

import avant_acte
from tests import aide_garde as ag

NL = chr(10)
LECTEUR = NL.join(["import sys", "with open(sys.argv[1] + '/.github/workflows/w.yml') as f:",
                   "    sys.exit(0 if f.read() == 'on: push' + chr(10) else 1)", ""])
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

    def horloge(self, iso):
        """Horloge fixée par un faux `date` en tête du PATH."""
        ag.ecrire(os.path.join(self.tmp, "faux"), {"date": "#!/bin/sh" + NL + "echo " + iso + NL})
        os.chmod(os.path.join(self.tmp, "faux", "date"), 0o755)
        os.environ["PATH"] = os.path.join(self.tmp, "faux") + os.pathsep + os.environ["PATH"]

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


    def test_e1_commit(self):
        """E1 : workflow indexé, lecteur YAML du dépôt en refus : refus C8 ; lecteur absent : erreur 3."""
        self.assertEqual(self.verifier({".github/workflows/w.yml": "on: push" + NL})[0], 3)
        code, sortie = self.verifier({"enforcement/workflows-yaml.py": LECTEUR,
                                      ".github/workflows/w.yml": "on: push: x" + NL})
        self.assertEqual((code, sortie[:9]), (1, "REFUS C8 "))
        self.assertEqual(self.verifier({".github/workflows/w.yml": "on: push" + NL}), (0, ""))


class DiffDeWorker(Source):
    def setUp(self):
        super().setUp()
        self.indexer({"JOURNAL.md": NL.join(["l1", "l2", "l3", "l4", "l5", ""]), "biblio/INDEX.md": "# index" + NL,
                      "enforcement/workflows-yaml.py": LECTEUR, ".github/workflows/w.yml": "on: push" + NL})
        ag.git(self.d, self.env, "commit", "-q", "-m", "base")
        self.w = os.path.join(self.tmp, "w.diff")

    def diff_de(self, fichiers):
        """Diff d'un worker : copie du dépôt, fichiers écrits et indexés, git diff --cached (contexte de 3 lignes)."""
        c = os.path.join(self.tmp, "copie")
        shutil.rmtree(c, ignore_errors=True)
        shutil.copytree(self.d, c)
        ag.ecrire(c, fichiers)
        ag.git(c, self.env, "add", "-A")
        ag.ecrire(self.tmp, {"w.diff": ag.git(c, self.env, "diff", "--cached", "HEAD")})
        return self.lancer("diff", "--fichier", self.w)

    def test_e21_e14_e16_e9(self):
        """Diff de worker reçu avant la G2 : E21, insertion au milieu d'un fichier cité (refus C7 ; ajout en fin
        admis) ; E14, heure future ; E16, citation stricte fausse ; E9, message d'outil anglais entre guillemets."""
        code, sortie = self.diff_de({"JOURNAL.md": NL.join(["l1", "l2", "neuf", "l3", "l4", "l5", ""])})
        self.assertEqual((code, sortie[:31]), (1, "REFUS C7 : JOURNAL.md : un bloc"))
        self.assertEqual(self.diff_de({"JOURNAL.md": NL.join(["l1", "l2", "l3", "l4", "l5", "fin", ""])}), (0, ""))
        faux = os.path.join(self.tmp, "faux")
        ag.ecrire(faux, {"date": "#!/bin/sh" + NL + "echo 2026-10-10T04:14:00Z" + NL})
        os.chmod(os.path.join(faux, "date"), 0o755)
        os.environ["PATH"] = faux + os.pathsep + os.environ["PATH"]
        g, d = chr(171), chr(187)
        for ligne, refus in [("page du 2026-10-10 04:22", "REFUS C4 : heure-future à n.md:2"),
                             (g + " l9 " + d + " (JOURNAL.md:2)", "REFUS C5 : citation-absente à n.md:2"),
                             (g + " fatal: not a git repository (or any of the parent directories) " + d,
                              "REFUS G5 : n.md:2 : fatal: not a git")]:
            code, sortie = self.diff_de({"n.md": "x" + NL + ligne + NL})
            self.assertEqual((code, sortie[:len(refus)]), (1, refus), ligne)

    def test_e1_interdit_tete(self):
        """E1 : workflow du diff illisible en YAML : refus C8 ; fichier du diff sous un interdit : refus, jamais
        nommé ; diff qui ne s'applique pas sur la tête (base ancienne) : refus."""
        self.assertEqual(self.diff_de({".github/workflows/w.yml": "on: push: x" + NL})[1][:9], "REFUS C8 ")
        code, sortie = self.diff_de({"docs/rapports/r.md": "x" + NL})
        self.assertEqual((code, sortie[:9], "rapports" in sortie), (1, "REFUS D1 ", False))
        self.diff_de({"JOURNAL.md": NL.join(["L1", "l2", "l3", "l4", "l5", ""])})
        self.indexer({"JOURNAL.md": NL.join(["autre", "l2", "l3", "l4", "l5", ""])})
        ag.git(self.d, self.env, "commit", "-q", "-m", "autre")
        self.assertEqual(self.lancer("diff", "--fichier", self.w)[1][:9], "REFUS D2 ")


class Versement(Depot):
    ADJ = "Adjudication de l'orchestrateur, section datée. " * 12

    def setUp(self):
        super().setUp()
        ag.ecrire(self.d, {"biblio/INDEX.md": "# index" + NL})
        self.p = os.path.join(self.tmp, "versement", "revue-x")

    def verser(self, pieces, sommes=None):
        """Pièces écrites dans un dossier du scratchpad, SHA256SUMS écrit depuis le dossier (forme exigée), sauf
        `sommes` donné."""
        shutil.rmtree(self.p, ignore_errors=True)
        ag.ecrire(self.p, pieces)
        if sommes is None:
            sommes = "".join(f"{hashlib.sha256(x.encode()).hexdigest()}  {n}" + NL for n, x in sorted(pieces.items()))
        ag.ecrire(self.p, {"SHA256SUMS": sommes})
        return self.lancer("verser", "--pieces", self.p)

    def test_e9_e10(self):
        """E9 : message d'outil anglais entre guillemets dans une pièce : refus G5 ; E10 : adjudication versée deux
        fois (même sha256, ou copie entière dans une autre pièce) : refus V2 ; pièces saines : sortie 0."""
        self.assertEqual(self.verser({"ADJUDICATION-extrait.md": self.ADJ, "G2-transcrit.md": "Relecture G2." + NL}),
                         (0, ""))
        e9 = chr(171) + " fatal: not a git repository (or any of the parent directories) " + chr(187)
        code, sortie = self.verser({"G2-transcrit.md": "Refus : " + e9 + NL})
        self.assertEqual((code, sortie[:47]), (1, "REFUS G5 : G2-transcrit.md:1 : fatal: not a git"))
        code, sortie = self.verser({"ADJUDICATION-extrait.md": self.ADJ, "G2-transcrit.md": "# G2" + NL + self.ADJ})
        self.assertEqual((code, sortie[:9]), (1, "REFUS V2 "))
        self.assertEqual(self.verser({"a.md": "court", "b.md": "court"})[1][:9], "REFUS V2 ")
        self.assertEqual(self.verser({"a.md": self.ADJ[:400], "b.md": "x " + self.ADJ[:400]}), (0, ""))

    def test_sommes_chemins_heures(self):
        """V4 : SHA256SUMS écrit avec ./, ligne fausse, pièce non listée, absent : refus ; V3 : chemin absolu du
        scratchpad dans une pièce : refus ; heure future (C4) ; fichier sous un interdit : refus sans le nommer."""
        h = hashlib.sha256(b"x").hexdigest()
        for pieces, sommes in [({"a.md": "x"}, h + "  ./a.md" + NL), ({"a.md": "y"}, h + "  a.md" + NL),
                               ({"a.md": "x", "b.md": "y"}, h + "  a.md" + NL)]:
            self.assertEqual(self.verser(pieces, sommes)[1][:9], "REFUS V4 ", sommes)
        os.remove(os.path.join(self.p, "SHA256SUMS"))
        self.assertEqual(self.lancer("verser", "--pieces", self.p)[1][:9], "REFUS V4 ")
        self.assertEqual(self.verser({"a.md": "voir /tmp/claude-0/projet/session/scratchpad/x"})[1][:9], "REFUS V3 ")
        self.horloge("2026-10-10T04:14:00Z")
        self.assertEqual(self.verser({"a.md": "le 2026-10-10 04:22"})[1][:9], "REFUS C4 ")
        code, sortie = self.verser({"docs/rapports/r.md": "x"})
        self.assertEqual((code, sortie[:9], "rapports" in sortie), (1, "REFUS V0 ", False))


class Poussee(Depot):
    def pousser(self, *argv):
        return self.lancer("pousser", "--distant", "origin", "--branche", "b", *argv)

    def test_la_n05_et_hors_distant(self):
        """LA-N05 : poussée sans sceau de la tête : refus P1 ; scellée : admise ; docs 15/16 dans la plage poussée, ou
        dans la tête d'une branche neuve : refus P2, fichier jamais nommé ; workflow illisible poussé : refus C8."""
        ag.git(self.d, self.env, "update-ref", "refs/remotes/origin/b", "HEAD")
        self.assertEqual(self.pousser()[1][:9], "REFUS P1 ")
        self.lancer("sceller", "--tete")
        self.assertEqual(self.pousser(), (0, ""))
        self.indexer({"docs/15-poche.md": "x" + NL})
        ag.git(self.d, self.env, "commit", "-q", "-m", "poche")
        self.lancer("sceller", "--tete")
        code, sortie = self.pousser()
        self.assertEqual((code, sortie[:9], "poche" in sortie), (1, "REFUS P2 ", False))
        ag.git(self.d, self.env, "update-ref", "refs/remotes/origin/b", "HEAD")
        self.assertEqual(self.pousser(), (0, ""))
        self.assertEqual(self.lancer("pousser", "--distant", "origin", "--branche", "neuve")[1][:9], "REFUS P2 ")
        self.indexer({"enforcement/workflows-yaml.py": LECTEUR, ".github/workflows/w.yml": "on: push: x" + NL})
        ag.git(self.d, self.env, "commit", "-q", "-m", "w")
        self.lancer("sceller", "--tete")
        self.assertEqual(self.pousser()[1][:9], "REFUS C8 ")

    def test_e17_actes_refuses(self):
        """E17 : écritures que le mandataire refuse (protection, réglages, suppression de branche) : refus P4 avant
        tout essai ; une lecture des réglages : admise ; une ligne chemin n'est pas un motif d'acte."""
        for acte in ["gh api -X PUT repos/o/r/branches/main/protection --input p.json",
                     "gh api -X PATCH repos/o/r -f security_and_analysis[secret_scanning][status]=enabled",
                     "git push origin --delete essai/analyseur-residus"]:
            self.assertEqual(self.lancer("pousser", "--acte", acte)[1][:9], "REFUS P4 ", acte)
        self.assertEqual(self.lancer("pousser", "--acte", "gh api repos/o/r/branches/main/protection"), (0, ""))
        self.assertEqual(self.lancer("pousser", "--acte", "docs/15-x"), (0, ""))
        self.assertEqual(self.lancer("pousser")[0], 3)

    def test_e14_publier(self):
        """E14 : heure future dans un texte publié (04:22 à 04:14) : refus C4 ; motif de secret de la gate G3 : refus,
        jamais recopié ; chemin du scratchpad : refus V3 ; texte sain : admis."""
        self.horloge("2026-10-10T04:14:00Z")
        cle = "AKIA" + "ABCDEFGHIJKLMNOP"
        for texte, code in [("Fusion du 2026-10-10 04:22.", "REFUS C4 "), ("clé " + cle, "REFUS P5 "),
                            ("voir /tmp/claude-0/p/s/scratchpad/x", "REFUS V3 ")]:
            ag.ecrire(self.tmp, {"texte.md": texte + NL})
            sortie = self.lancer("publier", "--texte", os.path.join(self.tmp, "texte.md"))[1]
            self.assertEqual((sortie[:9], cle in sortie), (code, False), texte)
        ag.ecrire(self.tmp, {"texte.md": "Fusion du 2026-10-10 04:13." + NL})
        self.assertEqual(self.lancer("publier", "--texte", os.path.join(self.tmp, "texte.md")), (0, ""))


class ExisteDisque(Depot):
    def libre(self, gio):
        usage = collections.namedtuple("usage", "total used free")
        return mock.patch.object(avant_acte.GC.shutil, "disk_usage", return_value=usage(1, 1, int(gio * 2 ** 30)))

    def test_e15_existe(self):
        """E15 : WISHLIST.md cherché sous biblio/ alors qu'il est à la racine : existe le trouve partout (suivi ou non),
        jamais sous un interdit ; nom absent : refus ; chemin ou motif : erreur."""
        self.indexer({"WISHLIST.md": "x", "biblio/INDEX.md": "x"})
        ag.ecrire(self.d, {"sous/WISHLIST.md": "x", "docs/rapports/WISHLIST.md": "x"})
        self.assertEqual(self.lancer("existe", "WISHLIST.md"), (0, "WISHLIST.md" + NL + "sous/WISHLIST.md" + NL))
        self.assertEqual(self.lancer("existe", "ABSENT.md")[:2], (1, "REFUS X1 : ABSENT.md absent du dépôt "
                                                                     "(suivis et non suivis, hors interdits)" + NL))
        self.assertEqual([self.lancer("existe", x)[0] for x in ("biblio/INDEX.md", "*.md")], [3, 3])

    def test_e4_disque(self):
        """E4 : 2,9 Gio libres : refus ; 4 : avertissement ; 7 : rien ; --min-go 8 serre ; --lister : cibles cargo
        (CACHEDIR.TAG) à profondeur 4 au plus, sans docs, lien ni dossier sans étiquette ; racine dangereuse (ancêtre
        du dépôt, dossier docs) : 3."""
        for gio, argv, attendu in [(2.9, [], (1, "REFUS DQ")), (4, [], (0, "AVERTISSEMENT DQ")), (7, [], (0, "")),
                                   (7, ["--min-go", "8"], (1, "REFUS DQ"))]:
            with self.libre(gio):
                code, sortie = self.lancer("disque", *argv)
            self.assertEqual((code, sortie[:len(attendu[1])]), attendu, (gio, argv))
        s = os.path.join(self.tmp, "s")
        for chemin in ["lot1/copie/target/CACHEDIR.TAG", "lot2/target/x", "docs/x/target/CACHEDIR.TAG",
                       "a/b/c/d/target/CACHEDIR.TAG", "lot1/copie/target/debug/gros"]:
            ag.ecrire(s, {chemin: "x" * 1024})
        os.symlink(os.path.join(s, "lot1"), os.path.join(s, "lien"))
        with self.libre(7):
            code, sortie = self.lancer("disque", "--lister", s)
            dangereuses = [self.lancer("disque", "--lister", x)[0] for x in (self.tmp, os.path.join(s, "docs"))]
        self.assertEqual(dangereuses, [3, 3])
        self.assertEqual((code, sortie), (0, "0.00 Gio" + chr(9) + os.path.join(s, "lot1", "copie", "target") + NL))


class PlanDeChaine(Depot):
    def juger(self, groupes, *pas, options=()):
        """Plan d'une ligne par pas (diffs nommés par leur fichier) et rapport de contre-contrôle à la ligne fixe."""
        plan = [f"P-{i}|" + ",".join(f"/s/{d}.diff" for d in x) + "|/s/m.txt|/s/ADJ.md" for i, x in enumerate(pas)]
        ag.ecrire(self.tmp, {"plan": NL.join(plan) + NL, "cc.md": "# Contre-contrôle" + NL + groupes + NL})
        return self.lancer("chaine", "--plan", os.path.join(self.tmp, "plan"), "--cc", os.path.join(self.tmp, "cc.md"),
                           *options)

    def test_e11_groupe_coupe(self):
        """E11 : FZ-x rouge seul, groupé avec FZ-i au rapport : plan qui les commet en deux pas, refus G2 ; en un pas,
        admis ; rapport sans ligne GROUPES, avec deux, ou ligne illisible : refus G1 ; GROUPES : aucun : admis."""
        code, sortie = self.juger("GROUPES : FZ-x+FZ-i", ["FZ-a"], ["FZ-x"], ["FZ-i", "FZ-g"])
        self.assertEqual((code, sortie[:9], "FZ-x+FZ-i" in sortie), (1, "REFUS G2 ", True))
        self.assertEqual(self.juger("GROUPES : FZ-x+FZ-i ; FZ-g+FZ-h", ["FZ-a"], ["FZ-x", "FZ-i"]), (0, ""))
        self.assertEqual(self.juger("Groupes : voir le tableau", ["FZ-x"])[1][:9], "REFUS G1 ")
        self.assertEqual(self.juger("GROUPES : FZ-x+", ["FZ-x"])[1][:9], "REFUS G1 ")
        self.assertEqual(self.juger("GROUPES : aucun" + NL + "GROUPES : FZ-x+FZ-i", ["FZ-x"])[1][:9], "REFUS G1 ")
        self.assertEqual(self.juger("GROUPES : aucun", ["FZ-x"], ["FZ-i"]), (0, ""))

    def test_e25_duree(self):
        """E25 : 23 commits à 6 min par défaut (138 min) en lancement lié : refus G3, lancement détaché donné ;
        détaché : admis ; 16 pas (96 min) : admis ; durée mesurée de 8 min et 13 pas (104 min) : refus."""
        pas = [[f"D-{i}"] for i in range(23)]
        code, sortie = self.juger("GROUPES : aucun", *pas)
        self.assertEqual((code, sortie[:9], "setsid nohup" in sortie, "138 min" in sortie),
                         (1, "REFUS G3 ", True, True))
        self.assertEqual(self.juger("GROUPES : aucun", *pas, options=["--detache"]), (0, ""))
        self.assertEqual(self.juger("GROUPES : aucun", *pas[:16]), (0, ""))
        self.assertEqual(self.juger("GROUPES : aucun", *pas[:13], options=["--duree-pas", "8"])[1][:9], "REFUS G3 ")
