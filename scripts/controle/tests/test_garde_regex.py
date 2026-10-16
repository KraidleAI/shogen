"""Cas du lint des motifs (lot GARDE-FOUS-ORCH, phase 2, groupe A ; annexe B, B.102, SHOGEN-GARDE-OUTIL-E6-E7-E12-E13-1 ;
erreur E12 : alerte CodeQL py/redos sur VIDE et BLOC de enforcement/runners-epingles.py, corrigés par DT5-24). Les motifs
portent des barres obliques inverses : écrits depuis chr(92), jamais tapés (SHOGEN-HARNAIS-ECHAPPEMENTS-1)."""
import unittest

import garde_commun as gc

B = chr(92)
S, ESP = B + "S", B + "s"
AVANT_DT5_24 = {"VIDE": ESP + "*(?:[&!]" + S + "*" + ESP + "*)*", "BLOC": ESP + "*(?:[&!]" + S + "*" + ESP + "*)*[|>][-+0-9]*"
                + ESP + "*"}
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
                    "(?:a+b|ac)*": "alternatives-ambigues", "(.+)+": "quantificateurs-imbriques"}
        self.assertEqual({m: gc.motifs_suspects(m) for m in signales}, {m: [c] for m, c in signales.items()})
        surs = ["SHOGEN-[A-Z0-9]+(?:-[A-Z0-9]+)*", "(?:[0-9a-f]{2})*", "(a+b)*", "(?:ab|a)*", "(?:x|xa)*",
                "(?:foo|bar)*", "(a+){2,5}", "(?:xy|xz)*", "(?:[ab]c|a)*", "a.*b",
                B + "bgit(?:" + ESP + "+(?:-C" + ESP + "+" + S + "+|--no-optional-locks|--git-dir=" + S + "+))*"]
        self.assertEqual({m: gc.motifs_suspects(m) for m in surs}, {m: [] for m in surs})
        self.assertEqual(gc.motifs_suspects("(a"), ["motif-illisible"])
