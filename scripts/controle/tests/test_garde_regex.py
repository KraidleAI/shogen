"""Cas du lint des motifs (lot GARDE-FOUS-ORCH, phase 2, groupe A ; annexe B, B.102, SHOGEN-GARDE-OUTIL-E6-E7-E12-E13-1 ;
erreur E12 : alerte CodeQL py/redos sur VIDE et BLOC de enforcement/runners-epingles.py, corrigés par DT5-24). Les motifs
portent des barres obliques inverses : écrits depuis chr(92), jamais tapés (SHOGEN-HARNAIS-ECHAPPEMENTS-1)."""
import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

import avant_acte
import garde_commun as gc
from tests import aide_garde as ag

B = chr(92)
S, ESP = B + "S", B + "s"
AVANT_DT5_24 = {"VIDE": ESP + "*(?:[&!]" + S + "*" + ESP + "*)*", "BLOC": ESP + "*(?:[&!]" + S + "*" + ESP + "*)*[|>][-+0-9]*"
                + ESP + "*"}
NL = chr(10)
APRES_DT5_24 = {"VIDE": ESP + "*(?:[&!]" + S + "*" + ESP + "+)*(?:[&!]" + S + "*)?",
                "BLOC": ESP + "*(?:[&!]" + S + "*" + ESP + "+)*(?:[&!]" + S + "*)?[|>][-+0-9]*" + ESP + "*"}


class Motifs(unittest.TestCase):
    def test_e12_motifs_de_dt5(self):
        """E12 : VIDE et BLOC d'avant DT5-24 (l.25-26 du fichier à e7ffd12) : quantificateurs imbriqués ; réécrits par
        DT5-24 (mêmes chaînes acceptées) : rien de suspect."""
        self.assertEqual({k: gc.motifs_suspects(v) for k, v in AVANT_DT5_24.items()},
                         {"VIDE": ["quantificateurs-imbriques"], "BLOC": ["quantificateurs-imbriques"]})
        self.assertEqual({k: gc.motifs_suspects(v) for k, v in APRES_DT5_24.items()}, {"VIDE": [], "BLOC": []})

    def test_e12_formes(self):
        """Formes exponentielles connues signalées (répétition variable en queue, alternative de largeur variable en
        queue, branches inséparables ou vides, borne haute > 10, sous une assertion, point) ; formes sûres voisines non
        signalées (corps à séparateur, largeur fixe, préfixe strict séparé, borne haute ≤ 10) ; motif illisible."""
        signales = {"^(a+)+$": "quantificateurs-imbriques", "(a{1,2})*": "quantificateurs-imbriques",
                    "(" + ESP + "*," + ESP + "*)*": "quantificateurs-imbriques",
                    "(?:[a-z]+|[0-9]+)*": "quantificateurs-imbriques", "(a+){1,50}": "quantificateurs-imbriques",
                    "(?=(a+)+b)": "quantificateurs-imbriques", "(a|aa)*$": "alternatives-ambigues",
                    "(?:a|b|ab)*": "alternatives-ambigues", "(ab|ab)*$": "alternatives-ambigues",
                    "(?:a+b|ac)*": "alternatives-ambigues", "(.+)+": "quantificateurs-imbriques",
                    "(.*,)*": "quantificateurs-imbriques", "((?:.*),)*$": "quantificateurs-imbriques",
                    "(?i)(?:A+a+)+$": "quantificateurs-imbriques", "x(?i:A+a+)+": "quantificateurs-imbriques"}
        self.assertEqual({m: gc.motifs_suspects(m) for m in signales}, {m: [c] for m, c in signales.items()})
        surs = ["SHOGEN-[A-Z0-9]+(?:-[A-Z0-9]+)*", "(?:[0-9a-f]{2})*", "(a+b)*", "(?:ab|a)*", "(?:x|xa)*",
                "(?:foo|bar)*", "(a+){2,5}", "(?:xy|xz)*", "(?:[ab]c|a)*", "a.*b", "(?:A+a+)+$",
                B + "bgit(?:" + ESP + "+(?:-C" + ESP + "+" + S + "+|--no-optional-locks|--git-dir=" + S + "+))*"]
        self.assertEqual({m: gc.motifs_suspects(m) for m in surs}, {m: [] for m in surs})
        self.assertEqual(gc.motifs_suspects("(a"), ["motif-illisible"])


class Branchement(unittest.TestCase):
    """RX : motifs des lignes ajoutées, à la réception d'un diff (diff), au commit (index) et à la poussée (plage),
    dans un dépôt git temporaire isolé ; DT5-7 a ajouté VIDE en forme exponentielle, DT5-24 l'a réécrit."""
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.tmp = t.name
        self.d, self.env = ag.depot(self.tmp, {"r.py": "import re" + NL, "w.yml": "on: push" + NL})
        env = mock.patch.dict(os.environ, self.env, clear=True)
        env.start()
        self.addCleanup(env.stop)

    def lancer(self, *argv):
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(io.StringIO()):
            code = avant_acte.main(["--depot", self.d, *argv])
        return code, [x.split(" ; à faire")[0] for x in sortie.getvalue().split(NL)[:-1] if x[:7] in ("REFUS R",
                                                                                                    "ADMIS R", "AVERTIS")]

    def diff_de(self, fichiers):
        ag.ecrire(self.d, fichiers)
        texte = ag.git(self.d, self.env, "diff")
        ag.git(self.d, self.env, "checkout", "--", ".")
        chemin = os.path.join(self.tmp, "x.diff")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(texte)
        return self.lancer("diff", "--fichier", chemin)

    def test_e12_rx_diff_commit_pousser(self):
        """E12 : VIDE exponentiel ajouté (DT5-7) : refus RX au diff, au commit et à la poussée ; réécrit par DT5-24 :
        rien ; grep et clé pattern d'un workflow ; redos-admis : admis ; concaténation : non lue ; illisible : avis."""
        vide = "VIDE = re.compile(r" + chr(34) + AVANT_DT5_24["VIDE"] + chr(34) + ")"
        refus = ["REFUS RX : r.py:2 : motif à retour arrière exponentiel (quantificateurs-imbriques) (E12)"]
        self.assertEqual(self.diff_de({"r.py": "import re" + NL + vide + NL}), (1, refus))
        ag.ecrire(self.d, {"r.py": "import re" + NL + vide + NL})
        ag.git(self.d, self.env, "commit", "-q", "-am", "DT5-7")
        sain = "VIDE = re.compile(r" + chr(34) + APRES_DT5_24["VIDE"] + chr(34) + ")"
        self.assertEqual(self.diff_de({"r.py": "import re" + NL + sain + NL}), (0, []))
        code, lignes = self.lancer("pousser", "--distant", "origin", "--branche", "main")
        self.assertEqual((code, [x for x in lignes if "RX" in x]), (1, refus))
        ag.ecrire(self.d, {"r.py": "import re" + NL + vide + NL + "B = re.compile(" + chr(34) + "(a+)+" + chr(34) + ")"
                           + NL, "m.txt": "x" + NL})
        ag.git(self.d, self.env, "add", "r.py")
        code, lignes = self.lancer("commit", "--message", os.path.join(self.d, "m.txt"), "--source",
                                   os.path.join(self.d, "m.txt"))
        self.assertEqual([x for x in lignes if "RX" in x], [refus[0].replace("r.py:2", "r.py:3")])
        ag.git(self.d, self.env, "reset", "-q", "--hard")
        self.assertEqual(self.diff_de({"w.yml": "on: push" + NL + "  run: grep -E '(b+)+' f" + NL + "pattern: (c*)*"
                                       + NL})[1], [x.replace("r.py:2", "w.yml:" + n) for n in "23" for x in refus])
        self.assertEqual(self.diff_de({"r.py": "import re" + NL + "C = re.compile('(a+)+')  # redos-admis : essai" + NL
                                       + "D = re.compile('(a+)+' + E)" + NL + "F = re.search('(a', x)" + NL}),
                         (0, ["ADMIS RX : r.py:2 : quantificateurs-imbriques, admis par redos-admis",
                              "AVERTISSEMENT RX : r.py:4 : motif illisible par re, non jugé"]))


class Arbre(unittest.TestCase):
    """SHOGEN-MOTIFS-ARBRE-REDOS-1 (annexe B, B.109) : motifs --arbre juge les motifs déjà dans l'arbre, dans une copie
    (dépôt git temporaire isolé) où des motifs suspects sont plantés."""
    def test_motifs_arbre(self):
        """Plantés sous scripts/controle/, .claude/hooks/ et enforcement/ : concaténation de noms et de chr(92), drapeaux
        re.I et re.X, sep.join, appel sur deux lignes, clé YAML : refus RX à leur ligne ; redos-admis (sur la dernière ligne d'un
        appel sur deux lignes compris) : admis ; motif fait d'une variable : NON-LU ; code illisible : avertissement ;
        hors des trois dossiers ou sous __pycache__ : non jugé. G2, C-5 : méthode d'un motif compilé (SAIN.search) dont
        l'argument est un sujet, non un motif : non jugée."""
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        q = chr(34)
        d, env = ag.depot(t.name, {
            "scripts/controle/x.py": NL.join(["import re", "B = chr(92)", "SAIN = re.compile(" + q + "[a-z]+" + q + ")",
                                              "MAUVAIS = re.compile(" + q + "(?:" + q + " + B + " + q + "s*," + q + " + B + "
                                              + q + "s*)*$" + q + ")", "VAR = re.compile(motif)",
                                              "CASSE = re.compile(" + q + "(?:A+a+)+$" + q + ", re.I)",
                                              "JOINT = re.search(" + q + q + ".join([" + q + "(a+)" + q + ", " + q + "+" + q
                                              + "]), x)", "VERB = re.compile(" + q + "(a +)+" + q + ", re.X)",
                                              "SUJET = SAIN.search(" + q + "(a+)+" + q + ")", ""]),
            ".claude/hooks/h.py": NL.join(["import re", "NOM = re.compile(r" + q + "(a+)" + q, "                 r" + q
                                           + "+$" + q + ")", "ADMIS = re.compile(" + q + "(b+)+" + q + ")  # redos-admis",
                                           "DEUX = re.compile(" + q + "(c+)" + q, "                  " + q + "+$" + q
                                           + ")  # redos-admis", ""]),
            "scripts/controle/__pycache__/z.py": "import re" + NL + "Z = re.compile(" + q + "(a+)+" + q + ")" + NL,
            "enforcement/w.yml": "pattern: '(a|aa)*$'" + NL, "enforcement/c.py": "def f(:" + NL,
            "scripts/autre.py": "import re" + NL + "X = re.compile(" + q + "(a+)+" + q + ")" + NL})
        sortie = io.StringIO()
        with mock.patch.dict(os.environ, env, clear=True), contextlib.redirect_stdout(sortie):
            code = avant_acte.main(["--depot", d, "motifs", "--arbre"])
        refus = "REFUS RX : {} : motif à retour arrière exponentiel ({}) (E12)"
        self.assertEqual((code, [x.split(" ; à faire")[0] for x in sortie.getvalue().split(NL)[:-1]]), (1, [
            "NON-LU scripts/controle/x.py:5 : motif construit hors littéraux, non jugé",
            "motifs --arbre : 9 motif(s) lu(s), 1 non lu(s), dossiers scripts/controle, .claude/hooks, enforcement",
            "AVERTISSEMENT RX : enforcement/c.py : code illisible par ast, non jugé",
            refus.format("scripts/controle/x.py:4", "quantificateurs-imbriques"),
            refus.format("scripts/controle/x.py:6", "quantificateurs-imbriques"),
            refus.format("scripts/controle/x.py:7", "quantificateurs-imbriques"),
            refus.format("scripts/controle/x.py:8", "quantificateurs-imbriques"),
            refus.format(".claude/hooks/h.py:2", "quantificateurs-imbriques"),
            "ADMIS RX : .claude/hooks/h.py:4 : quantificateurs-imbriques, admis par redos-admis",
            "ADMIS RX : .claude/hooks/h.py:5 : quantificateurs-imbriques, admis par redos-admis",
            refus.format("enforcement/w.yml:1", "alternatives-ambigues")]))
