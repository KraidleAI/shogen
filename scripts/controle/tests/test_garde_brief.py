"""Cas du contrôle des briefs (lot GARDE-FOUS-ORCH, phase 2, groupe A ; annexe B, B.102 :
SHOGEN-GARDE-OUTIL-E6-E7-E12-E13-1, SHOGEN-GARDE-OUTIL-E22-E23-E24-1), dans des dépôts git temporaires isolés
(tests/aide_garde.py), jamais le dépôt du projet ; rouges sur l'erreur réelle reproduite, verts sur le cas sain.
E6 : brief FUZZ qui citait SHOGEN-E1-XTASK-REFS-1 ouvert, fermé par XR-1 à XR-4 (annexe B l.819-822 et l.1583, lignes
copiées à l'octet dans ANNEXE_E6). E24 : brief DETTES-T7 sans la règle des commandes git à chemins explicites."""
import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

import avant_acte
import garde_commun as gc
from tests import aide_garde as ag

NL = chr(10)
ANNEXE_E6 = NL.join([
    "Items **fermés** (commits D8d-1 `ba9d61a`, D8d-2 `44fec62`, G5 `27189d7`, RUNNERS `26c2c41`, XR-1 `1c2f0f2`, XR-2 "
    "`ef657b9`, XR-3 `7c4861a`, XR-4 `c278b48`) : SHOGEN-D8D-SECRETS-1 avec SHOGEN-SECRETS-CHEMIN-ETAGE-1, "
    "SHOGEN-SECRETS-GREP-STATUT-1,",
    "SHOGEN-SECRETS-MASQUE-EXCLUSION-1, SHOGEN-SECRETS-MESSAGES-1 ; SHOGEN-SECRETS-HORS-REFS-1 (reste un acte local : "
    "`--hors-refs`",
    "avant toute copie brute de `.git` en custodie, ADR-0028 §4.11) ; SHOGEN-G5-ERREUR-GREP-1 ; SHOGEN-E1-XTASK-REFS-1 "
    "(gate S-G9",
    "sur `docs/17`, contrôles (a) à (f) ; (g) et (h) déclarés non mécanisés). **Reste ouvert** : SHOGEN-CI-RUNNERS-1 "
    "(part Linux", ""])
LIGNE_1583 = ("- SHOGEN-E1-XTASK-REFS-1 : déjà fermé par XR-1 à XR-4 (lot DETTES-B2) ; la preuve rejouée par le générateur "
              "à `094fa5d` (8 neutralisations de S-G9, toutes tuées) est versée avec le rapport.")
ANNEXE = os.path.join("docs", "adr-0028", "ANNEXE-B-items.md")


class EtatItems(unittest.TestCase):
    def test_e6_etat_des_items(self):
        """Portée d'un en-tête « Items fermés … : » sur le paragraphe ; reste ouvert ; mot fermé après l'item ; cellule
        de tableau ; négation ; en-tête sans fermeture ; dernière décision ; item sans décision : ouvert."""
        e = gc.etat_items(ANNEXE_E6 + LIGNE_1583)
        self.assertEqual([e[x] for x in ("SHOGEN-D8D-SECRETS-1", "SHOGEN-E1-XTASK-REFS-1", "SHOGEN-CI-RUNNERS-1")],
                         [("fermé", 1), ("fermé", 5), ("ouvert", 4)])
        self.assertEqual(gc.etat_items(ANNEXE_E6)["SHOGEN-E1-XTASK-REFS-1"], ("fermé", 3))
        texte = NL.join(["| SHOGEN-A-1 | constat | orch. | **fermé** au commit |", "| SHOGEN-B-1 | fermé | x |",
                         "SHOGEN-C-1 non clos ; SHOGEN-D-1 **fermé** ; SHOGEN-E-1 reste **ouvert**.",
                         "Items précisés : SHOGEN-F-1.", "Items **fermés** :", "- SHOGEN-G-1 : fait.", "",
                         "SHOGEN-H-1 (suite).", "MONARK-S2-I-1 — fermé.", "SHOGEN-D-1 rouvert."])
        self.assertEqual({k: v[0] for k, v in gc.etat_items(texte).items()},
                         {"SHOGEN-A-1": "fermé", "SHOGEN-B-1": "fermé", "SHOGEN-C-1": "ouvert", "SHOGEN-D-1": "ouvert",
                          "SHOGEN-E-1": "ouvert", "SHOGEN-F-1": "ouvert", "SHOGEN-G-1": "fermé", "SHOGEN-H-1": "ouvert",
                          "MONARK-S2-I-1": "fermé"})


class Brief(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.tmp = t.name
        self.d, self.env = ag.depot(self.tmp, {ANNEXE: ANNEXE_E6 + LIGNE_1583 + NL,
                                               ".claude/agents/fiche-regle.md": "Toute commande git qui liste ou "
                                               "compare des chemins est limitée à une liste" + NL + "explicite de "
                                               "chemins." + NL, ".claude/agents/fiche-nue.md": "x" + NL})
        env = mock.patch.dict(os.environ, self.env, clear=True)
        env.start()
        self.addCleanup(env.stop)

    def brief(self, texte, *options):
        chemin = os.path.join(self.tmp, "BRIEF.md")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(texte)
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(io.StringIO()):
            code = avant_acte.main(["--depot", self.d, "brief", "--texte", chemin, *options])
        return code, sortie.getvalue()

    def test_e6_item_ferme_cite_ouvert(self):
        """E6 : item fermé à l'annexe cité ouvert : refus B1 avec la ligne de la décision ; écrit fermé dans le brief,
        ou ouvert à l'annexe : conforme ; absent de l'annexe : avertissement seul."""
        code, sortie = self.brief("Items ouverts à traiter : SHOGEN-E1-XTASK-REFS-1 (S-G9 sur les autres documents) ; "
                                  "SHOGEN-CI-RUNNERS-1." + NL)
        self.assertEqual((code, sortie.split(NL)[:-1]), (1, ["REFUS B1 : SHOGEN-E1-XTASK-REFS-1 cité ouvert ; fermé à "
                         "l'annexe B l.5 (E6) ; à faire : relire la ligne de l'annexe, retirer l'item du brief ou "
                         "l'écrire fermé"]))
        self.assertEqual(self.brief("SHOGEN-E1-XTASK-REFS-1 est fermé (XR-1 à XR-4)." + NL), (0, ""))
        self.assertEqual(self.brief("Reprendre SHOGEN-INCONNU-1." + NL),
                         (0, "AVERTISSEMENT B1 : SHOGEN-INCONNU-1 absent de l'annexe B" + NL))

    def test_e24_git_sans_regle(self):
        """E24 : brief qui nomme une commande git (copie creuse, git diff --numstat) sans la règle : refus B4 ; la règle
        au brief, ou à la fiche nommée par --fiche (lignes repliées) : conforme ; fiche sans la règle : refus ; fiche
        absente ou nom hors forme : erreur 3 ; brief sans git : conforme."""
        texte = "Travaille sur une copie creuse ; compte les lignes par `git diff --numstat`." + NL
        code, sortie = self.brief(texte)
        self.assertEqual((code, sortie[:9]), (1, "REFUS B4 "))
        self.assertEqual(self.brief(texte + "Toute commande git est limitée à une liste explicite de chemins." + NL),
                         (0, ""))
        self.assertEqual(self.brief(texte, "--fiche", "fiche-regle"), (0, ""))
        self.assertEqual(self.brief(texte, "--fiche", "fiche-nue")[0], 1)
        self.assertEqual([self.brief(texte, "--fiche", x)[0] for x in ("absente", "../agents/fiche-regle")], [3, 3])
        self.assertEqual(self.brief("Aucune commande à lancer." + NL), (0, ""))
        self.assertEqual(self.brief("Lis les commandes git du journal." + NL)[0], 1)
