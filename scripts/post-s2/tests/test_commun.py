"""Commun du lot POST-PREREG : étiquette, portée du J28, lecture du bloc 3 du rendu, contrôle de cohérence.
Attendus écrits à la main ; chaque test nomme la mutation qui le rougit."""
import importlib.util
import os
import tempfile
import unittest
from decimal import Decimal

import commun
from shogen_s2 import r1
from tests import fixtures as fx


def analyse(d):
    return ["ANALYSE"]


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

    def test_chargeur_egal_au_point_d_entree_scelle(self):
        """10 fenêtres calmes (vendredi 23:50-23:59) et 10 de stress ; plage [23:52 ; 23:53] ; n fixe 18 ; e mort en
        stress (D1 cas b) : n = 8 et 8, pool de stress a-d. Rougit si le chargeur oublie le segment, la plage ou D1."""
        ws = [fx.VEN + 86400 - 600 + 60 * i for i in range(20)]
        fx.journaux(self.d, ws, lambda i, f: "panne_transport" if (f == "e" and i >= 10) or (f in "ab" and i % 3 == 0)
                    else "ok")
        c, j = (os.path.join(self.d, n) for n in ("control.jsonl", "journal.jsonl"))
        seg, plages = {"t0": ws[0], "n_fixe": 18}, [(ws[2], ws[3])]
        d = commun.charger(self.d, seg, plages)
        self.assertEqual(d["base"], r1.recompute_from_journal(c, j, plages, seg))
        self.assertEqual((d["base"]["strates"]["calme"]["n"], d["base"]["strates"]["stress"]["n"]), (8, 8))
        self.assertEqual(d["pools"]["stress"], ["a", "b", "c", "d"])

    def test_executer_fail_closed_etiquette_en_tete(self):
        """3 fenêtres calmes : a et b en panne à la 1re, a seule à la 2e : n = 3, K = 1, p̂ = (2/3, 1/3, 0, 0, 0),
        P̂_more = 2/9 (à la main). Rougit si l'écart ne ferme pas la sortie (code 1, aucune ligne d'analyse) ou si
        l'étiquette n'est pas en première ligne."""
        fx.journaux(self.d, [fx.VEN + 60 * i for i in range(3)],
                    lambda i, f: "panne_transport" if (i == 0 and f in "ab") or (i == 1 and f == "a") else "ok")
        sortie, argv = os.path.join(self.d, "s.txt"), ["--journaux", self.d, "--t0", str(fx.VEN), "--n-fixe", "3",
                                                         "--plage", "0", "0"]
        for k, code in ((1, 0), (2, 1)):
            r = rendu(os.path.join(self.d, f"r{k}.out"), {"calme": (3, k, "0." + "2" * 50)})
            self.assertEqual(commun.executer("essai", "ITEM", analyse, argv + ["--sortie", sortie, "--rendu", r]), code)
            with open(sortie, encoding="utf-8") as f:
                lignes = f.read().splitlines()
            self.assertEqual(lignes[0], commun.ETIQUETTE)
            self.assertEqual("ANALYSE" in lignes, code == 0)
            self.assertEqual(any("aucune valeur d'analyse" in x for x in lignes), code == 1)


if __name__ == "__main__":
    unittest.main()
