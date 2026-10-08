"""Socle du lot PLAN-S2BIS-2 : variable, schéma, épingles, sous-arbres, écarts (d), pool (c). Attendus écrits à la main
ou par sha256sum ; chaque test nomme la mutation qui le rougit."""
import json
import os
import shutil
import tempfile
import unittest

import socle
import tests


class TestSocle(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="p2_socle_")
        self.addCleanup(shutil.rmtree, self.d, True)

    def refus(self, code, f, *args):
        with self.assertRaises(socle.Refus) as c:
            f(*args)
        self.assertEqual(c.exception.code, code)

    def test_variable(self):
        """T-P2-SOC-2. Environnement passé en argument : la variable posée, même vide, refuse ; absente, aucun refus.
        Aucun test Python ne pose la variable. Mutation M-P2-02 : garde retirée ; M-P2R0-1 : garde sur la valeur."""
        for v in ("x", ""):
            self.refus("P2/variable", socle.garde, {"SHOGEN_S2_CAMPAGNE_CONTROL": v})
        self.assertIsNone(socle.garde({"AUTRE": "1"}))

    def test_schema(self):
        """T-P2-SOC-5. parametres.json du lot conforme ; clé en trop ou manquante (premier niveau ou imbriquée),
        flottant, booléen pour un entier (d ; un compte du masque), clé dupliquée, JSON illisible : P2/parametres.
        Mutation M-P2-35 : contrôle de schéma retiré ; M-P2R0-2 : sous-arbres non contrôlés ; M-P2R0-3 : clé dupliquée
        admise ; G-10 (G2) : booléen admis dans les comptes ; M-P2R0-9 : idem, par type ; M-P2R0-10 : calendrier hors
        D5 typé dict seul."""
        self.assertEqual(socle.lire(), tests.PRM)

        def variante(f):
            p = json.loads(json.dumps(tests.PRM))
            f(p)
            return json.dumps(p, ensure_ascii=False)
        cas = [variante(lambda p: p.update(autre="x")), variante(lambda p: p.pop("passes")),
               variante(lambda p: p["masque"].update(autre="x")), variante(lambda p: p["passes"].update(A=0.0)),
               variante(lambda p: p["masque"]["sautees_hors_d5"].update(calme=5701.0)),
               variante(lambda p: p["masque"]["calendrier_hors_d5"].update(calme=True)),
               variante(lambda p: p["voisinage"].update(d=True)), '{"lot": "x", ' + json.dumps(tests.PRM)[1:], "{"]
        for i, texte in enumerate(cas):
            with open(os.path.join(self.d, f"p{i}.json"), "w", encoding="utf-8") as f:
                f.write(texte)
            self.refus("P2/parametres", socle.lire, os.path.join(self.d, f"p{i}.json"))
