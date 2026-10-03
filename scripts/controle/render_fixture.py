"""Rendu de la fixture de test_exclusion (sans option, puis avec l'option PLAGE), sur l'arbre s2-harness donné.

Méthode du G1 de DOCS-S2 (docs/G1-lot-DOCS-S2.md l.79) : même fixture que les épingles SHA_BASE_SANS_OPTION
(test_exclusion iv) et SHA_BASE_AVEC_OPTION (test_pool_analyse, épingle) ; écrit les deux rendus et imprime leurs
sha256. Usage : python -B render_fixture.py <arbre s2-harness> <dossier de sortie>
"""
import hashlib
import os
import sys
import tempfile

arbre, sortie = sys.argv[1], sys.argv[2]
sys.path.insert(0, arbre)
os.makedirs(sortie, exist_ok=True)
from shogen_s2 import report                           # noqa: E402
from tests.test_exclusion import PLAGE, build_fixture  # noqa: E402

assert os.path.dirname(os.path.dirname(os.path.abspath(report.__file__))) == os.path.abspath(arbre)
d = tempfile.mkdtemp(prefix="render_fixture_")
c, j = build_fixture(d)
for nom, rg in (("sans_option", ()), ("avec_option", [PLAGE])):
    txt = report.render_report(c, j, exclude_ranges=rg)
    with open(os.path.join(sortie, nom + ".txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(nom, hashlib.sha256(txt.encode("utf-8")).hexdigest())
