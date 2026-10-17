"""Cas de l'aide commune des tests (lot ISOLE-ENV, erreur E39 du registre de l'orchestrateur) : l'environnement des cas
n'hérite pas des variables de lancement d'une chaîne réelle, celles que lisent les modèles de gabarits/*.sh."""
import os
import tempfile
import unittest
from unittest import mock

from tests import aide_garde as ag
from tests import test_gabarit_chaine as tgc

# Référence indépendante de l'aide (règle 4 ; relecture G2 du lot ISOLE-ENV, C-1) : variables lues par les
# modèles de gabarits/, relevées par la relecture et recopiées ici ; un modèle neuf peut en ajouter (inclusion).
LUES = frozenset({"CC", "DELAI", "DEPOT", "DETACHE", "DISQUE_MIN_GO", "DUREE_PAS", "OUTILS", "PLAN", "PYTHON"})


class EnvironnementAmbiant(unittest.TestCase):
    def test_e39_variables_de_chaine_retirees(self):
        """E39 : chaque variable lue par un modèle de chaîne (dont DETACHE, cause de l'erreur) est retirée de
        l'environnement des cas, même posée dans l'environnement ambiant ; une variable étrangère aux modèles passe."""
        noms = ag.variables_de_chaine()
        self.assertLessEqual(LUES, noms)
        ambiant = dict({n: "1" for n in noms}, SHOGEN_E39_NEUTRE="garde")
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, ambiant):
            env = ag.env_git(d)
        self.assertEqual((sorted(noms & set(env)), env.get("SHOGEN_E39_NEUTRE")), ([], "garde"))

    def test_e39_lancement_lie_sous_lancement_detache(self):
        """E39, cas réel : test_e25_lancement_lie (refus d'un lancement lié trop long) rejoué sous DETACHE=1 et
        DUREE_PAS=60 posés dans l'environnement ambiant, comme pendant la vérification d'une chaîne lancée détachée : vert.
        Relecture G2, C-3 : ROUGE=X-1 ambiant (variable du faux verif des cas) ne rougit pas le premier pas."""
        cas = tgc.Chaine("test_e25_lancement_lie")
        with mock.patch.dict(os.environ, {"DETACHE": "1", "DUREE_PAS": "60", "ROUGE": "X-1"}):
            resultat = unittest.TestResult()
            cas.run(resultat)
        self.assertEqual((resultat.failures, resultat.errors, resultat.testsRun), ([], [], 1))


if __name__ == "__main__":
    unittest.main()
