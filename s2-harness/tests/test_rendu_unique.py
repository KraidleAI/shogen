"""SHOGEN-RENDU-UNIQUE-1 (G0 docs/adr-0028/G0-partie-2.md §C ; ADR-0028 annexe D.4 b) : tools/rendu_unique.py sur
dépôts git jetables (core.autocrlf=false ; fixtures seulement, D.4 a). Attendus indépendants de l'outil : sha256 des
octets écrits par le test, sha de git rev-parse, noms des gardes écrits à la main ; mutants par garde : journal G1."""
from __future__ import annotations

import hashlib
import importlib.util
import os
import unittest
from pathlib import Path

from tests.test_oracle_record import HARNESS

OUTIL = os.path.join(HARNESS, "tools", "rendu_unique.py")
_SPEC = importlib.util.spec_from_file_location("rendu_unique", OUTIL)
ru = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ru)
JOURNAUX = {"control.jsonl": b'{"type": "run_params"}\n', "journal.jsonl": b'{"v": 1}\n', "raw.jsonl": b'{"r": 2}\n'}


def h(octets: bytes) -> str:
    return hashlib.sha256(octets).hexdigest()


def lignes_bloc(c1: str, sommes: bytes) -> list:
    return [f"commit_analyse {c1}", f"sha256_script {h(Path(OUTIL).read_bytes())}",
            *(f"journal {n} {h(v)}" for n, v in JOURNAUX.items()), f"sommes {h(sommes)}",
            "cacert_sha256 " + "1" * 64, "tsa_crt_sha256 " + "2" * 64]


def texte_bloc(lignes: list) -> str:
    return "# Paquet de fixture\n\n```shogen-paquet-v1\n" + "\n".join(lignes) + "\n```\n"


class TestRenduUnique(unittest.TestCase):
    def test_bloc_absent_duplique_malforme(self):
        """Bloc machine (G0 §C), lecteur seul : forme nominale lue à l'identique ; chaque variante absente, dupliquée ou
        malformée lève ValueError. Rougit si : clé dupliquée admise (même valeur), clé ou journal absent, quatrième
        journal, majuscules, sha tronqué, champ en trop, clé inconnue, nom hors forme admis ; second bloc ou
        ouverture voisine ignorés ; fermeture non exigée."""
        x = lignes_bloc("a" * 40, b"s")
        self.assertEqual(ru.lire_bloc(texte_bloc(x)), {
            "commit_analyse": "a" * 40, "sha256_script": h(Path(OUTIL).read_bytes()), "sommes": h(b"s"),
            "cacert_sha256": "1" * 64, "tsa_crt_sha256": "2" * 64, "journal": {n: h(v) for n, v in JOURNAUX.items()}})
        for nom, lignes in (("clé absente", x[:5] + x[6:]), ("journal absent", x[:4] + x[5:]),
                            ("quatre journaux", x + ["journal autre.jsonl " + "3" * 64]), ("clé dupliquée", x + [x[1]]),
                            ("journal dupliqué", x[:5] + [x[2]] + x[5:]),
                            ("majuscules", [x[0], x[1][:14] + x[1][14:].upper(), *x[2:]]),
                            ("sha tronqué", [x[0], x[1][:-1], *x[2:]]), ("commit court", [x[0][:-1], *x[1:]]),
                            ("champ en trop", [x[0], x[1] + " x", *x[2:]]), ("clé inconnue", x + ["autre " + "4" * 64]),
                            ("tabulation", [x[0].replace(" ", "\t"), *x[1:]]), ("ligne vide", x + [""]),
                            ("retour chariot", [x[0] + "\r", *x[1:]]),
                            ("nom hors forme", [*x[:2], "journal ../c " + "5" * 64, *x[3:]])):
            with self.subTest(variante=nom), self.assertRaises(ValueError):
                ru.lire_bloc(texte_bloc(lignes))
        t = texte_bloc(x)
        for nom, texte in (("aucun bloc", "# Paquet\n"), ("deux blocs", t + t), ("non fermé", t[:-4]),
                           ("ouverture voisine", t + "\n~~~ shogen-paquet-v1\n~~~\n"),
                           ("ouverture tilde", t.replace("```shogen", "~~~shogen").replace("\n```\n", "\n~~~\n"))):
            with self.subTest(variante=nom), self.assertRaisesRegex(ValueError, "ouverture"):
                ru.lire_bloc(texte)


if __name__ == "__main__":
    unittest.main()
