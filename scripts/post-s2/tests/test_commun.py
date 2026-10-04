"""Commun du lot POST-PREREG : étiquette, portée du J28, lecture du bloc 3 du rendu, contrôle de cohérence.
Attendus écrits à la main ; chaque test nomme la mutation qui le rougit."""
import importlib.util
import os
import tempfile
import unittest
from decimal import Decimal

import commun


def rendu(chemin, valeurs):
    """Faux rendu réduit au bloc 3 : {strate : (n, K, P̂_more en chaîne)} ; chaque strate porte aussi une ligne de
    strate poolée (« P̂_more = » à un espace), qui ne doit pas être lue."""
    lignes = ["[ÉTIQUETTE] j28", "[BLOC 3] R1"]
    for st, (n, k, p) in valeurs.items():
        lignes += [f"  ── strate « {st} » : n = {n} fenêtres complétées ; K = {k} (fenêtres à ≥ 2 écarts)",
                   f"    P̂_more  = {p}", f"    « {st} » : n = {n} ; K = {k} ; P̂_more = 0.5 ; pool = 5 flux"]
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes + ["[BLOC 4] L&M"]) + "\n")
    return chemin


class TestCommun(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="pp_commun_")

    def test_etiquette_mot_pour_mot(self):
        """Rougit si un caractère de l'étiquette imposée par le brief change."""
        self.assertEqual(commun.ETIQUETTE, "ajoutée après le pré-enregistrement, hors décision ; ne change pas le "
                                           "verdict de la règle scellée (« R1 discrimine » = FAUX, docs/11 §3)")

    def test_portee_egale_a_la_table_du_rendu(self):
        """Rougit si t0, n fixe ou la plage D5 diffèrent de la sortie « j28 » de rendu_unique.SORTIES."""
        spec = importlib.util.spec_from_file_location("ru", os.path.join(commun.HARNAIS, "tools", "rendu_unique.py"))
        ru = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ru)
        (_nom, seg, plages, _etiquette), = [s for s in ru.SORTIES if s[0] == "j28"]
        self.assertEqual((seg, plages), (commun.SEGMENT, (commun.PLAGE_D5,)))

    def test_lire_bloc3_ignore_la_strate_poolee(self):
        """Rougit si la ligne de strate poolée (P̂_more = 0.5) est lue à la place de celle de la strate."""
        r = rendu(os.path.join(self.d, "r.out"), {"calme": (24585, 154, "0.0013"), "stress": (11397, 133, "0.0014")})
        self.assertEqual(commun.lire_bloc3(r), {"calme": (24585, 154, "0.0013"), "stress": (11397, 133, "0.0014")})

    def test_controle_j28_egal_ecart_et_strate_manquante(self):
        """P̂_more = 2/9 à 50 chiffres (« 0.2…2 », écrit à la main). Rougit si une différence de K, de P̂_more ou une
        strate absente du recompte passe pour égale."""
        b = {"strates": {"calme": {"n": 3, "K": 1, "P_more": Decimal("0." + "2" * 50)}}}
        bon = rendu(os.path.join(self.d, "a.out"), {"calme": (3, 1, "0." + "2" * 50)})
        self.assertEqual(commun.controle_j28(b, bon)[0], True)
        for k, v in enumerate(((3, 2, "0." + "2" * 50), (3, 1, "0." + "2" * 49 + "3")), 1):
            self.assertEqual(commun.controle_j28(b, rendu(os.path.join(self.d, f"e{k}.out"), {"calme": v}))[0], False)
        deux = rendu(os.path.join(self.d, "s.out"), {"calme": (3, 1, "0." + "2" * 50), "stress": (1, 0, "0")})
        ok, lignes = commun.controle_j28(b, deux)
        self.assertEqual((ok, lignes[1].endswith("ÉCART")), (False, True))


if __name__ == "__main__":
    unittest.main()
