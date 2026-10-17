"""Cas de SHOGEN-GARDE-REPONSE-INVESTISSEUR-1 (GARDE-FOUS phase 3, groupe B ; annexe B, B.108 ; E29) : règle R12 du
crochet GARDE-FAITS, au Stop. Chaque nombre à unité de la réponse (jours, semaines, mois, heures, minutes, ans, %,
commits, tests, fichiers) doit figurer, avec une forme de son unité sur la même ligne, dans un résultat d'outil ou une
pièce du tour (fenêtre : depuis le dernier message de l'humain, ce message compris) ; sinon refus qui nomme le nombre.
R6 n'est pas touchée. Crochet chargé par son chemin, joué en processus sur un journal synthétique (nom en .txt)."""
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
# Ligne 158 de docs/adr-0029/ADR-0029-campagne-S2-bis.md (§2.4 (e)), extrait recopié tel quel (lu par grep -n) :
ADR_E = ("158:**(e) Cellule cible, n par strate et durée.** […] à la cible, 12 semaines donnent 0,77 et 16 semaines "
         "0,91 (tableau (d) [calc, synthétique]).")


def charger():
    spec = importlib.util.spec_from_file_location("garde_faits_r12", GARDE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def humain(texte):
    return {"type": "user", "message": {"role": "user", "content": texte}}


def outil(i, commande, resultat):
    return [{"type": "assistant", "message": {"content": [{"type": "tool_use", "id": f"t{i}", "name": "Bash",
                                                            "input": {"command": commande}}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": f"t{i}",
                                                      "content": resultat}]}}]


def reponse(texte):
    return {"type": "assistant", "uuid": "u-" + texte[:8], "message": {"content": [{"type": "text", "text": texte}]}}


class ReponseInvestisseur(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.t, self.g = t.name, charger()

    def arreter(self, entrees, ev="Stop", actif=False):
        """(sortie, stderr) du crochet sur un arrêt après les entrées du journal."""
        j = os.path.join(self.t, "journal.txt")
        with open(j, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(e) + NL for e in entrees)
        e = {"hook_event_name": ev, "transcript_path": j, "cwd": self.t, "stop_hook_active": actif}
        err = io.StringIO()
        with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(e))), contextlib.redirect_stderr(err):
            code = self.g.main()
        return code, err.getvalue()

    def test_e29_vingt_huit_jours_sans_piece(self):
        """Cas réel E29 : « Pendant les 28 jours de collecte » sans pièce lue ; un 28 affiché sans son unité (R6 le
        tient pour affiché) : refus R12 qui nomme le nombre ; au second arrêt du tour : passage consigné."""
        tour = [humain("Quelle durée pour la collecte ?"), *outil(1, "grep -n collecte notes.txt", "28:collecte"),
                reponse("Pendant les 28 jours de collecte, rien ne change.")]
        code, err = self.arreter(tour)
        self.assertEqual((code, "R12" in err, "28 jours" in err), (2, True, True), err)
        self.assertEqual(self.arreter(tour, actif=True), (0, ""))
        with open(os.path.join(self.t, "garde-faits.log"), encoding="utf-8") as f:
            self.assertIn("PASSAGE R12", f.read())
        double = [humain("Bilan ?"), *outil(1, "grep -n collecte notes.txt", "28:collecte"),
                  reponse("Il reste 28 jours ; 123 cas.")]        # G2, C-3 : R6 refuse 123, R12 juge aussi 28 jours
        code, err = self.arreter(double)
        self.assertEqual((code, "R6" in err, "R12" in err, "28 jours" in err), (2, True, True, True), err)
        r10 = [humain("Réponds à CoinGecko."), *outil(1, "grep -n collecte notes.txt", "28:collecte"),
               reponse("Pour Pocket, il reste 28 jours.")]        # G2, C-3 : R10 refuse Pocket, R12 juge aussi 28 jours
        code, err = self.arreter(r10)
        self.assertEqual((code, "R10" in err, "R12" in err), (2, True, True), err)

    def test_e29_seize_semaines_apres_lecture(self):
        """16 semaines après lecture de la pièce ADR-0029 §2.4 (e) dans le tour : permis ; forme anglaise de l'unité
        et unité sur la même ligne (tableau) : permis ; % accolé : permis."""
        lu = outil(1, "grep -n '16 semaines' docs/adr-0029/ADR-0029-campagne-S2-bis.md", ADR_E)
        self.assertEqual(self.arreter([humain("Durée ?"), *lu, reponse("La campagne dure 16 semaines.")]), (0, ""))
        avant = reponse("Je vérifie les 28 jours.")        # texte d'avant le dernier appel d'outil : hors réponse
        self.assertEqual(self.arreter([humain("Durée ?"), avant, *lu, reponse("16 semaines.")]), (0, ""))
        compte = [humain("Série ?"), *outil(1, "git log --oneline a..b | wc -l", "5"), reponse("Elle compte 5 commits.")]
        self.assertEqual(self.arreter(compte), (0, ""))        # G2, C-4 : compte lu par wc -l (R5, C-6 ; E7)
        for piece, texte in (("16 weeks of data", "Elle dure 16 semaines."), ("| durée | 16 | semaines |",
                             "Elle dure 16 semaines."), ("évaluables : 95%", "Seuil : 95 % des fenêtres.")):
            self.assertEqual(self.arreter([humain("Durée ?"), *outil(1, "cat p", piece), reponse(texte)]), (0, ""),
                             piece)

    def test_unite_et_fenetre(self):
        """Refus : nombre affiché avec une autre unité sur sa ligne ; pièce lue avant le dernier message de l'humain
        (hors fenêtre) ; message de l'humain du tour qui porte le nombre : permis ; SubagentStop : R12 ne juge pas.
        Nombre et unité sur deux lignes d'un même résultat : refus (CC de l'intégration P3, R-4)."""
        code, err = self.arreter([humain("x ?"), *outil(1, "cat p", "28 tests verts"), reponse("Il reste 28 jours.")])
        self.assertEqual((code, "28 jours" in err), (2, True), err)
        refus = "GARDE-FAITS : REFUS. R5 : 28 jours"        # un refus du crochet n'est jamais une pièce
        code, err = self.arreter([humain("x ?"), *outil(1, "cat p", refus), *outil(2, "cat q", "28:collecte"),
                                  reponse("Il reste 28 jours.")])
        self.assertEqual((code, "28 jours" in err), (2, True), err)
        avant = [humain("Durée ?"), *outil(1, "cat p", ADR_E), reponse("16 semaines."), humain("Et donc ?")]
        code, err = self.arreter([*avant, reponse("Toujours 16 semaines.")])
        self.assertEqual((code, "16 semaines" in err), (2, True), err)
        self.assertEqual(self.arreter([humain("Tu dis 16 semaines ?"), reponse("Oui, 16 semaines.")]), (0, ""))
        code, err = self.arreter([humain("Où en est J28 ?"), reponse("Pendant les 28 jours de collecte.")])
        self.assertEqual((code, "R12" in err), (2, True), err)      # G2, C-2 : R6 couvre 28 par J28 (B-2), R12 refuse
        tour = [humain("x ?"), *outil(1, "cat p", "28:collecte"), reponse("Pendant les 28 jours.")]
        self.assertEqual(self.arreter(tour, ev="SubagentStop"), (0, ""))
        code, err = self.arreter([humain("x ?"), *outil(1, "grep -c x f", "28"), reponse("Il reste 28 jours.")])
        self.assertEqual((code, "28 jours" in err), (2, True), err)        # G2, C-4 : un compte n'est pas une durée
        ancien = [humain("Série ?"), *outil(1, "git log --oneline | wc -l", "5"), reponse("Vu."), humain("Et donc ?")]
        code, err = self.arreter([*ancien, reponse("Elle compte 5 commits.")])
        self.assertEqual((code, "5 commits" in err), (2, True), err)        # G2, C-4 : compte d'un tour antérieur
        lignes = outil(1, "cat p", "28:collecte" + NL + "fenêtre en jours")
        code, err = self.arreter([humain("x ?"), *lignes, reponse("Il reste 28 jours.")])
        self.assertEqual((code, "28 jours" in err), (2, True), err)        # CC de l'intégration P3, R-4 : même ligne
        voisins = outil(1, "cat p", "280 jours ; 28,5 jours")
        code, err = self.arreter([humain("x ?"), *voisins, reponse("Il reste 28 jours.")])
        self.assertEqual((code, "28 jours" in err), (2, True), err)        # G2, C-5 : 280 et 28,5 ne portent pas 28


if __name__ == "__main__":
    unittest.main()
