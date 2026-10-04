# -*- coding: utf-8 -*-
"""Lanceur des tests du lot DOCS11-EN, au contrat des runners du projet (SHOGEN-MUT-FATAL-1).

Usage : python3 -B lancer_tests.py DOSSIER_DES_MODULES
Sortie : 0 tous les tests passent ; 1 au moins un test échoue (aucune erreur) ; 3 erreur fatale (import, erreur
d'exécution d'un test, aucun test lancé). Le dossier des modules passe en tête du chemin d'import : c'est ainsi
qu'un module factice ou un mutant remplace le module réel.
"""
import os
import sys
import unittest


def main(argv):
    if len(argv) != 1 or not os.path.isdir(argv[0]):
        print("usage : lancer_tests.py DOSSIER_DES_MODULES")
        return 3
    modules = os.path.abspath(argv[0])
    tests = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, modules)
    chargeur = unittest.TestLoader()
    suite = chargeur.discover(start_dir=tests, pattern="test_*.py", top_level_dir=tests)
    resultat = unittest.TextTestRunner(verbosity=1).run(suite)
    if chargeur.errors or resultat.errors:
        return 3
    if resultat.testsRun == 0:
        return 3
    if resultat.failures:
        noms = sorted({t.id().split(".")[-1] for t, _ in resultat.failures})
        print("tests en échec : " + ", ".join(noms))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
