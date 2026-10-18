"""RB-2 : fusion des journaux des quatre observateurs (E-R-03, E-R-04 ; Q-R-03 ; témoin et remplaçants). Journaux
synthétiques seulement, écrits par l'écrivain de collecte/journal.py ; `run_params` par le câblage de collecte/entree.py
(`configurer`, `configurer_secondaire`, `_liste`, `_run_params`) sur les configurations de production et des
descripteurs d'essai ; aucun journal de campagne. Attendus écrits ici (listes, codes nommés, sha256 par hashlib sur les
octets des fichiers), indépendants du code de la fusion."""
import hashlib
import os
import shutil
import tempfile
import unittest

from shogen_s2bis.recalc import fusion

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(RACINE, "config")
COMMIT = "c" * 40
WS = 1791158220                         # 2026-10-04 23:57 UTC (`date -u -d @1791158220`)
OBS = ("o1", "o2", "o3", "o4")          # liste fermée d'observateurs.json (GEL-7)
SANTE = {"d2": {"retard_max": 0, "non_parties": 0}}           # `sante` d'essai, sans sondes


def sha(chemin):
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class Paquet(unittest.TestCase):                            # quatre fichiers lus en octets ; liste fermée
    def test_quatre_fichiers_lus_en_octets(self):
        lus = fusion.paquet(CONFIG)
        self.assertEqual(({n: lus[n][1] for n in lus}, lus["observateurs"][0]), (
            {n: sha(os.path.join(CONFIG, n + ".json")) for n in ("formes", "sante", "observateurs", "carte")},
            {"observateurs": list(OBS)}))
        with tempfile.TemporaryDirectory() as d:
            for n in ("formes", "sante", "observateurs", "carte"):
                shutil.copy(os.path.join(CONFIG, n + ".json"), d)
            for octets in (b"{", b'{"formes": "' + bytes([255]) + b'"}'):     # JSON coupé ; chaîne hors UTF-8
                with open(os.path.join(d, "carte.json"), "wb") as f:
                    f.write(octets)
                with self.assertRaises(fusion.RefusFusion) as e:
                    fusion.paquet(d)
                self.assertEqual(e.exception.code, "FUSION/config")

    def test_liste_fermee(self):
        """Observateurs lus autres que la liste fermée (o1 à o4) : refus, avant toute lecture (dossiers absents)."""
        with tempfile.TemporaryDirectory() as base:
            d = {o: os.path.join(base, o) for o in OBS}
            cinq = os.path.join(base, "o5")
            for lus in ({o: d[o] for o in OBS[:3]}, {**d, "o5": cinq}, {**{o: d[o] for o in OBS[:3]}, "o5": cinq},
                        {**d, "O1": d["o1"]}, {}):
                with self.subTest(lus=sorted(lus)):
                    with self.assertRaises(fusion.RefusFusion) as e:
                        fusion.Fusion(lus, CONFIG, COMMIT)
                    self.assertEqual(e.exception.code, "FUSION/observateurs")
