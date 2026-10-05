"""RB-1 : lecteur en flux des journaux (E-R-01, E-R-02 ; FORMAT §1 à §8). Lignes fabriquées ici (`ligne`, de
tests/test_reprise.py) ; empreintes par hashlib sur les octets du test."""
import hashlib
import os
import sys
import tempfile
import unittest

from shogen_s2bis.recalc import lecteur as lec
from tests.test_reprise import ligne, m

OUVERTURE = ligne(0, "0" * 64, type="ouverture", jour="2026-10-04", suivante=m(1))
P = hashlib.sha256(OUVERTURE).hexdigest()


class LigneIntegre(unittest.TestCase):                      # FORMAT §7.1 ; écrivain de référence : `_lire`
    def test_lignes_integres_et_etat(self):
        e, etat = lec._integre(OUVERTURE, None)
        lecture = ligne(1, P, type="lecture", ws=m(1), k=1)
        e2, etat2 = lec._integre(lecture, etat)
        trou = ligne(2, etat2[1], type="trou", de=m(2), a=m(3), cause="saut")
        self.assertEqual((e["type"], etat, e2["k"], etat2, lec._integre(trou, etat2)[1]), (
            "ouverture", (1, P, m(1), None), 1, (2, hashlib.sha256(lecture).hexdigest(), m(1), m(1)),
            (3, hashlib.sha256(trou).hexdigest(), m(3), m(1))))

    def test_causes_nommees(self):
        etat = lec._integre(OUVERTURE, None)[1]
        lect = {"type": "lecture", "ws": m(1)}
        for cause, octets, avant in (("LECTEUR/fin", OUVERTURE[:-1], None), ("LECTEUR/json", bytes(9) + b"\n", etat),
                                     ("LECTEUR/json", b"[" * 100000 + b"]" * 100000 + b"\n", etat),
                                     ("LECTEUR/canonique", ligne(1, P, (", ", ": "), **lect), etat),
                                     ("LECTEUR/chaine", ligne(1, "0" * 64, **lect), etat),
                                     ("LECTEUR/chaine", ligne(2, P, **lect), etat),
                                     ("LECTEUR/chaine", ligne(0, "0" * 64, **lect), None),       # première ligne
                                     ("LECTEUR/champ", ligne(1, P, type="lecture", ws="23:02"), etat),
                                     ("LECTEUR/champ", ligne(1, P, type="marqueur", ws=True), etat),
                                     ("LECTEUR/champ", ligne(1, P, ws=m(1)), etat),
                                     ("LECTEUR/champ", ligne(1, P, type="lecture"), etat),
                                     ("LECTEUR/champ", ligne(0, "0" * 64, type="ouverture"), None),
                                     ("LECTEUR/champ", ligne(0, "0" * 64, type="ouverture", suivante="x"), None),
                                     ("LECTEUR/flottant", ligne(1, P, x=0.5, **lect), etat),
                                     ("LECTEUR/flottant", ligne(1, P, x=float("nan"), **lect), etat),
                                     ("LECTEUR/entier-long", ligne(1, P, x=10 ** 640, **lect), etat)):
            with self.subTest(cause=cause, octets=octets[:50]):
                with self.assertRaises(lec._NonIntegre) as e:
                    lec._integre(octets, avant)
                self.assertEqual(e.exception.args[0], cause)

    def test_entier_de_640_chiffres_lu_641_nomme_quel_que_soit_le_reglage(self):
        etat, reglage = lec._integre(OUVERTURE, None)[1], sys.get_int_max_str_digits()
        lus = [ligne(1, P, type="lecture", ws=m(1), x=x) for x in (10 ** 639, -10 ** 639)]
        nommes = [ligne(1, P, type="lecture", ws=m(1), x=x) for x in (10 ** 640, -10 ** 640)]
        for limite in (0, 640, 4300):                           # 0 : sans limite ; 640 : plus petite limite admise
            sys.set_int_max_str_digits(limite)
            try:
                valeurs, causes = [lec._integre(x, etat)[0]["x"] for x in lus], []
                for x in nommes:
                    with self.assertRaises(lec._NonIntegre) as e:
                        lec._integre(x, etat)
                    causes.append(e.exception.args[0])
            finally:
                sys.set_int_max_str_digits(reglage)
            self.assertEqual((valeurs == [10 ** 639, -10 ** 639], causes), (True, ["LECTEUR/entier-long"] * 2), limite)


class Fichiers(unittest.TestCase):
    def test_ordre_de_la_chaine_et_journal_absent(self):  # segments en ordre numérique ; autres fichiers ignorés
        with tempfile.TemporaryDirectory() as d:
            for n in ("pool-2026-10-04-10.jsonl", "pool-2026-10-05-0.jsonl", "pool-2026-10-04-2.jsonl", "pool.sha256",
                      "pool.verrou", "secondaire-2026-10-04-0.jsonl", "pool-2026-10-04-1.jsonl.bak"):
                open(os.path.join(d, n), "wb").close()
            self.assertEqual(lec.Lecteur(d, "pool").fichiers(), ["pool-2026-10-04-2.jsonl", "pool-2026-10-04-10.jsonl",
                                                                 "pool-2026-10-05-0.jsonl"])
            with self.assertRaises(lec.RefusLecteur) as e:
                lec.Lecteur(d, "carte").fichiers()
            self.assertEqual(e.exception.code, "LECTEUR/absent")
