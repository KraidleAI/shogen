"""Cas du contrôle des briefs (lot GARDE-FOUS-ORCH, phase 2, groupe A ; annexe B, B.102 :
SHOGEN-GARDE-OUTIL-E6-E7-E12-E13-1, SHOGEN-GARDE-OUTIL-E22-E23-E24-1), dans des dépôts git temporaires isolés
(tests/aide_garde.py), jamais le dépôt du projet ; rouges sur l'erreur réelle reproduite, verts sur le cas sain.
E6 : brief FUZZ qui citait SHOGEN-E1-XTASK-REFS-1 ouvert, fermé par XR-1 à XR-4 (annexe B l.819-822 et l.1583, lignes
copiées à l'octet dans ANNEXE_E6). E24 : brief DETTES-T7 sans la règle des commandes git à chemins explicites.
E22 : message de reprise de DT6 (phase 4) qui relayait le test instable de DB-1 sans sa référence. E23 : acte écrit
sans vérifier que l'outil, le fichier ou le commit nommés existent (copie au Drive de la décision Q-A). E7 : lapsus
« deux gardes » (il y en avait trois) : compte d'un brief jamais affiché par un outil (crochet GARDE-FAITS, R5)."""
import contextlib
import io
import json
import os
import subprocess
import sys
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
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GARDE = os.path.join(RACINE, ".claude", "hooks", "garde_faits.py")      # crochet GARDE-FAITS du dépôt (R11)


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
        solde = NL.join(["- SHOGEN-SCEAU-OTS-1 **sans objet** : pour S2, l'absence d'ancre OpenTimestamps est une limite "
                         "écrite.", "Items proposés par le G1 et soldés par décision au G0 §C (ajout daté) : "
                         "SHOGEN-RENDU-ETIQUETTE-1 (Q4).", "", "SHOGEN-J-1 non soldé ; SHOGEN-K-1 tranché « non »."])
        self.assertEqual({k: v[0] for k, v in gc.etat_items(solde).items()},      # relecture G2, C-1 (annexe l.1500, l.405)
                         {"SHOGEN-SCEAU-OTS-1": "fermé", "SHOGEN-RENDU-ETIQUETTE-1": "fermé", "SHOGEN-J-1": "ouvert",
                          "SHOGEN-K-1": "ouvert"})


class Brief(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.tmp = t.name
        self.d, self.env = ag.depot(self.tmp, {ANNEXE: ANNEXE_E6 + LIGNE_1583 + NL,
                                               ".claude/agents/fiche-regle.md": "Toute commande git qui liste ou "
                                               "compare des chemins est limitée à une liste" + NL + "explicite de "
                                               "chemins." + NL, ".claude/agents/fiche-nue.md": "x" + NL,
                                               "notes/rapport.md": "a" + NL + "b" + NL + "c" + NL, "scripts/outil.py": ""})
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
        au brief : conforme ; à la seule fiche nommée par --fiche : refus qui nomme la fiche (C-2, décision de
        l'orchestrateur : le brief la porte lui-même) ; fiche absente ou nom hors forme : erreur 3 ; options globales de
        git : vues ; brief sans git : conforme."""
        texte = "Travaille sur une copie creuse ; compte les lignes par `git diff --numstat`." + NL
        code, sortie = self.brief(texte)
        self.assertEqual((code, sortie[:9]), (1, "REFUS B4 "))
        self.assertEqual(self.brief(texte + "Toute commande git est limitée à une liste explicite de chemins." + NL),
                         (0, ""))
        code, sortie = self.brief(texte, "--fiche", "fiche-regle")
        self.assertEqual((code, "lui-même" in sortie, "quelle que soit la fiche (fiche-regle)" in sortie), (1, True, True))
        self.assertEqual(self.brief(texte, "--fiche", "fiche-nue")[0], 1)
        self.assertEqual([self.brief("Lister par `git " + x + " ls-files -- a`." + NL)[0]
                          for x in ("--no-pager", "-c core.quotePath=false", "-C /x --git-dir=/x/.git")], [1, 1, 1])
        self.assertEqual([self.brief(texte, "--fiche", x)[0] for x in ("absente", "../agents/fiche-regle")], [3, 3])
        self.assertEqual(self.brief("Aucune commande à lancer." + NL), (0, ""))
        self.assertEqual(self.brief("Lis les commandes git du journal." + NL)[0], 1)

    def test_e22_constat_relaye_sans_reference(self):
        """E22 : constat d'un autre lot relayé sans fichier ni ligne : refus B2 ; référence sur la ligne ou la suivante,
        forme entre guillemets ou en code (citée, non relayée), sujet sans verbe de relais : conforme ; selon la G2 :
        refus ; sujet au pluriel, contre-contrôleur, verbe au pluriel, d'après : refus (C-3)."""
        code, sortie = self.brief("Reprise de DT6, phase 4 : le contre-contrôle de DB-1 a relevé un test instable ; le "
                                  "stabiliser." + NL)
        self.assertEqual((code, sortie.split(" : ")[:2]), (1, ["REFUS B2", "l.1"]))
        for sain in ("Le contre-contrôle de DB-1 a relevé un test instable (`notes/rapport.md:2`).",
                     "Le contre-contrôle de DB-1 a relevé un test instable" + NL + "(notes/rapport.md l.3).",
                     "Forme visée : « la G2 a trouvé… », `le CC dit`.", "Le générateur écrit les diffs."):
            self.assertEqual(self.brief(sain + NL), (0, ""), sain)
        self.assertEqual(self.brief("Selon la G2, tout passe." + NL)[0], 1)
        self.assertEqual([self.brief(x + NL)[0] for x in ("Le contre-contrôleur a relevé un test instable.", "Les "
                          "réviseurs ont trouvé deux défauts.", "Les avis signalent un écart.", "D'après la G2, tout passe.")],
                         [1, 1, 1, 1])

    def test_e23_faisabilite(self):
        """E23 : outil, fichier ou commit nommés absents, ligne hors du fichier, sous-commande inconnue : refus B3, un par
        nom ; chemin à produire, base inconnue, sha256 abrégé, interdit (jamais lu), noms présents : conformes."""
        tete = ag.git(self.d, self.env, "rev-parse", "HEAD")[:12]
        code, sortie = self.brief(NL.join([
            "Copier les octets au Drive par `scripts/copier_drive.py`.", "Relire notes/rapport.md:7 puis `/nulle/x.py`.",
            "Base : commit abc1234def.", "Lancer `avant_acte.py verifier`.", "Écrire `scripts/neuf.py`.",
            "Lire `scripts/outil.py`, notes/rapport.md:2-3, `sous/inconnu/x.md`, base " + tete + ".",
            "sha256 `c3f34927467031d8` ; `docs/rapports/x.md` ; `scripts/` ; `-C/x`.",
            "Relire notes/rapport.md l.9, `notes/rapport.md` l.2-3, notes/absent.md l.1.", ""]))
        self.assertEqual((code, [x.split(" ; à faire")[0] for x in sortie.split(NL)[:-1]]), (1, [
            "REFUS B3 : l.1 : scripts/copier_drive.py absent (E23)",
            "REFUS B3 : l.2 : notes/rapport.md:7 hors du fichier (3 lignes) (E23)",
            "REFUS B3 : l.2 : /nulle/x.py absent (E23)",
            "REFUS B3 : l.3 : abc1234def n'est pas un commit du dépôt (E23)",
            "REFUS B3 : l.4 : sous-commande avant_acte.py verifier inconnue (E23)",
            "REFUS B3 : l.8 : notes/rapport.md l.9 hors du fichier (3 lignes) (E23)",
            "REFUS B3 : l.8 : notes/absent.md absent (E23)"]))

    def crochet(self, consigne, fiche="fiche-regle", outil="Agent", champ="prompt"):
        """(sortie, stderr) du crochet GARDE-FAITS sur un appel Agent (ou outil, consigne dans le champ nommé), journal
        vide en .txt, dépôt du test en CLAUDE_PROJECT_DIR."""
        j = os.path.join(self.tmp, "journal.txt")
        open(j, "w", encoding="utf-8").close()
        e = {"hook_event_name": "PreToolUse", "transcript_path": j, "cwd": self.tmp, "tool_name": outil,
             "tool_input": {champ: consigne, "subagent_type": fiche, "description": "essai"}}
        p = subprocess.run([sys.executable, "-I", GARDE], input=json.dumps(e), capture_output=True, text=True,
                           timeout=60, env=dict(os.environ, CLAUDE_PROJECT_DIR=self.d))
        return p.returncode, p.stderr

    def test_r11_crochet_agent(self):
        """R11 : la consigne d'un agent nomme un brief (absolu ou relatif au dossier courant) qui échoue au contrôle :
        refus du crochet, refus de l'outil recopiés ; brief conforme : permis ; règle git portée par la seule fiche du
        type d'agent : refus qui nomme la fiche (C-2) ; brief absolu absent : refus ; consigne courte sans brief :
        permis ; consigne de plus de CONSIGNE_MAX caractères sans brief : refus, avec un brief nommé : jugée par lui (C-5)."""
        self.brief("Reprendre SHOGEN-E1-XTASK-REFS-1, ouvert ; `git diff --numstat`." + NL)
        code, err = self.crochet("Lis d'abord ton brief : " + os.path.join(self.tmp, "BRIEF.md") + ", puis exécute-le.")
        self.assertEqual((code, err.count("REFUS B1"), "quelle que soit la fiche (fiche-regle)" in err), (2, 1, True), err)
        self.assertEqual(self.crochet("Brief : BRIEF.md", fiche="fiche-nue")[1].count("R11 : le brief"), 1)
        self.brief("Reprendre SHOGEN-CI-RUNNERS-1 ; `git diff --numstat`, limité à une liste explicite de chemins." + NL)
        self.assertEqual([self.crochet("Brief : BRIEF.md", fiche=x)[0] for x in ("fiche-regle", "fiche-nue")], [0, 0])
        code, err = self.crochet("Brief : " + os.path.join(self.tmp, "BRIEF-absent.md"))
        self.assertEqual((code, "R11 : la consigne nomme un brief absent" in err), (2, True), err)
        self.assertEqual(self.crochet("Aucun fichier à lire."), (0, ""))
        longue = "Consigne écrite en ligne. " * 58      # 1508 caractères
        code, err = self.crochet(longue[:1500])
        self.assertEqual((len(longue), code), (1508, 0), err)
        code, err = self.crochet(longue)
        self.assertEqual((code, "R11 : consigne de 1508 caractères sans fichier BRIEF*.md" in err), (2, True), err)
        self.assertEqual(self.crochet(longue + " Brief : BRIEF.md")[0], 0)
        with open(os.path.join(self.tmp, "BRIEF-KO.md"), "w", encoding="utf-8") as f:      # C-8 : Workflow, autre champ
            f.write("Reprendre SHOGEN-E1-XTASK-REFS-1." + NL)
        code, err = self.crochet("Brief : BRIEF-KO.md", outil="Workflow", champ="script")
        self.assertEqual((code, "REFUS B1" in err), (2, True), err)


class Comptes(unittest.TestCase):
    """E7 : comptes à unité d'un brief écrit (Write, Edit, redirection du shell), jugés par le crochet GARDE-FAITS (R5)
    contre les sorties d'outils du journal synthétique (.txt)."""
    def crochet(self, resultats, outil, entree, humain=None):
        with tempfile.TemporaryDirectory() as t:
            j = os.path.join(t, "journal.txt")
            with open(j, "w", encoding="utf-8") as f:
                if humain:      # message de l'humain, en bloc texte (C-8)
                    f.write(json.dumps({"type": "user", "message": {"content": [{"type": "text", "text": humain}]}}) + NL)
                for k, r in enumerate(resultats):      # sortie, ou (commande, sortie) ; résultat apparié par l'id
                    cmd, r = r if isinstance(r, tuple) else ("true", r)
                    f.write(json.dumps({"type": "assistant", "message": {"content": [
                        {"type": "tool_use", "id": f"t{k}", "name": "Bash", "input": {"command": cmd}}]}}) + NL)
                    f.write(json.dumps({"type": "user", "message": {"content": [
                        {"type": "tool_result", "tool_use_id": f"t{k}", "content": r}]}}) + NL)
            e = {"hook_event_name": "PreToolUse", "transcript_path": j, "cwd": t, "tool_name": outil,
                 "tool_input": entree}
            p = subprocess.run([sys.executable, "-I", GARDE], input=json.dumps(e), capture_output=True, text=True,
                               timeout=60)
        return p.returncode, p.stderr

    def test_e7_comptes_du_brief(self):
        """E7 : « deux gardes » écrit dans un brief, l'outil a affiché trois gardes : refus ; affiché (en chiffres ou en
        lettres, unité au pluriel ou en anglais) : permis ; Ran N contre Ran affiché ; borne ; fichier hors brief ;
        Edit et heredoc du shell vers un BRIEF*.md ; compte lu sans unité par grep -c ou wc -l : permis, le même
        nombre affiché par une autre commande : refus (C-6)."""
        brief = {"file_path": "/x/BRIEF-CC.md", "content": "C-11 : vérifier les deux gardes de presg5 ; Ran 117 ; "
                 "chaque diff ≤ 200 lignes ; 3 fichiers touchés." + NL}
        sorties = ["Ran 117 tests in 2.1s", "trois gardes", "3 files changed"]
        code, err = self.crochet(sorties, "Write", brief)
        self.assertEqual((code, "« deux gardes »" in err, "E7" in err), (2, True, True), err)
        self.assertEqual(self.crochet(sorties + ["2 gardes"], "Write", brief), (0, ""))
        self.assertEqual(self.crochet(["Ran 116 tests", "2 gardes", "3 fichiers"], "Write", brief)[0], 2)
        self.assertEqual(self.crochet([], "Write", dict(brief, file_path="/x/NOTES.md")), (0, ""))
        self.assertEqual(self.crochet(["3 tests"], "Write", dict(brief, content="3 fichiers"))[0], 2)   # autre unité
        self.assertEqual(self.crochet(["deux gardes"], "Edit", {"file_path": "/x/BRIEF.md", "old_string": "x",
                                                                 "new_string": "les 2 gardes"}), (0, ""))
        self.assertEqual(self.crochet([], "Bash", {"command": "cat > /x/BRIEF.md <<'F'" + NL + "5 mutants" + NL + "F"})[0],
                         2)
        lu = dict(brief, content="Ajouter 12 tests ; relire 42 lignes ; 7 fichiers." + NL)
        comptage = [("grep -c 'def test_' x.py", "12"), ("wc -l x.py", "42 x.py"), ("grep -c a d/*.py", "d/a.py:7")]
        self.assertEqual(self.crochet(comptage, "Write", lu), (0, ""))
        self.assertEqual(self.crochet([("cat x.py", "12")] + comptage[1:], "Write", lu)[0], 2)
        quatre = dict(brief, content="Rejouer 4 mutants." + NL)
        self.assertEqual([self.crochet([], "Write", quatre, humain=x)[0] for x in ("Rejoue 4 mutants.", "Rejoue 4 cas.")],
                         [0, 2])      # compte tapé par l'humain, même unité (C-8)
