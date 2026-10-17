"""Cas de SHOGEN-GARDE-JOURNAL-LECTURE-SEULE-1 (GARDE-FOUS phase 3, groupe B ; annexe B, B.108) : chaque passage de
avant_acte.py --lecture-seule écrit une ligne au journal garde/lecture-seule.tsv des outils (heure lue par date -u,
sous-commande, tête du dépôt lu, verdict) ; le dépôt lu reste intact. Le journal des cas est détourné vers le dossier
temporaire du cas (Depot.setUp de test_avant_acte), jamais celui de l'arbre."""
import os
import unittest

import avant_acte
from tests import aide_garde as ag
from tests import test_avant_acte as ta

NL = chr(10)
HEURE = "2026-10-16T13:00:00Z"


class JournalLectureSeule(ta.Source):
    def setUp(self):
        """Dépôt de DiffDeWorker (JOURNAL.md cité par numéro), sans hériter de ses cas."""
        super().setUp()
        self.indexer({"JOURNAL.md": NL.join(["l1", "l2", "l3", "l4", "l5", ""]), "biblio/INDEX.md": "# index" + NL,
                      "enforcement/workflows-yaml.py": ta.LECTEUR, ".github/workflows/w.yml": "on: push" + NL})
        ag.git(self.d, self.env, "commit", "-q", "-m", "base")
        self.w = os.path.join(self.tmp, "w.diff")

    diff_de, etat = ta.DiffDeWorker.diff_de, ta.DiffDeWorker.etat

    def lignes(self):
        if not os.path.exists(avant_acte.JOURNAL_LS):
            return []
        with open(avant_acte.JOURNAL_LS, encoding="utf-8") as f:
            return [x.split(chr(9)) for x in f.read().split(NL) if x]

    def test_passages_journalises(self):
        """Mode courant : aucune ligne ; --lecture-seule : diff conforme, diff refusé (C7), sous-commande refusée
        (sceller : erreur 3), chacun une ligne heure, sous-commande, tête du dépôt lu (40 hexadécimaux), verdict ;
        dépôt lu inchangé."""
        self.horloge(HEURE)
        tete = ag.git(self.d, self.env, "rev-parse", "HEAD").strip()
        self.assertEqual(self.diff_de({"n.md": "x" + NL}), (0, ""))
        self.assertEqual(self.lignes(), [])
        avant = self.etat()
        self.assertEqual(self.lancer("--lecture-seule", "diff", "--fichier", self.w), (0, ""))
        self.diff_de({"JOURNAL.md": NL.join(["l1", "l2", "neuf", "l3", "l4", "l5", ""])})
        avant = self.etat()
        self.assertEqual(self.lancer("--lecture-seule", "diff", "--fichier", self.w)[0], 1)
        self.assertEqual(self.lancer("--lecture-seule", "sceller")[0], 3)
        self.assertEqual(self.etat(), avant)
        self.assertEqual(self.lignes(), [[HEURE, "diff", tete, "conforme"], [HEURE, "diff", tete, "refus"],
                                         [HEURE, "sceller", tete, "erreur"]])

    def test_journal_ignore_par_git(self):
        """Le journal de l'arbre (garde/lecture-seule.tsv des outils) est ignoré par le .gitignore de la racine : il
        ne salit pas l'arbre d'une chaîne qui tourne (git status --porcelain vide), lu dans un dépôt d'essai ; de même le
        journal des refus et son fichier temporaire (garde/.gitignore ; CC de l'intégration P3, R-4)."""
        racine = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        with open(os.path.join(racine, ".gitignore"), encoding="utf-8") as f:
            ag.ecrire(self.d, {".gitignore": f.read(), "scripts/controle/garde/lecture-seule.tsv": "x" + NL})
        with open(os.path.join(racine, "scripts", "controle", "garde", ".gitignore"), encoding="utf-8") as f:
            ag.ecrire(self.d, {"scripts/controle/garde/.gitignore": f.read(), "scripts/controle/garde/refus.tsv": "x" + NL,
                               "scripts/controle/garde/refus.tsv.4242.tmp": "x" + NL})
        ag.git(self.d, self.env, "add", ".gitignore", "scripts/controle/garde/.gitignore")
        ag.git(self.d, self.env, "commit", "-q", "-m", "gitignore")
        self.assertEqual(ag.git(self.d, self.env, "status", "--porcelain", "--untracked-files=all"), "")

    def test_journal_non_ecrit(self):
        """Journal impossible à écrire (un dossier à sa place) : sortie 3, jamais 0 ni 1."""
        os.makedirs(avant_acte.JOURNAL_LS)
        self.diff_de({"n.md": "x" + NL})
        self.assertEqual(self.lancer("--lecture-seule", "diff", "--fichier", self.w)[0], 3)


if __name__ == "__main__":
    unittest.main()
