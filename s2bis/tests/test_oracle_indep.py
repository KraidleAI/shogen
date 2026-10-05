"""RB-18, lecteur indépendant (E-R-33 ; PROPOSITION du G0 de RECALC-BIS l.396, l.486, l.539-540, l.551) : attendus
construits depuis le FORMAT (docs/adr-0029/s2bis/FORMAT-JOURNAUX-S2BIS.md), jamais depuis un autre lecteur. Lignes,
valeurs et noms écrits à la main ici ; barre oblique inverse et saut de ligne jamais tapés (chr(92), octet 10)."""
import os
import subprocess
import sys
import tempfile
import unittest

from shogen_s2bis.recalc import oracle_indep as o
from tests.test_fitness import violations

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BS, NL, PREC = chr(92), bytes((10,)), "ab" * 32


def ligne(texte):
    return texte.encode("utf-8") + NL


class Ligne(unittest.TestCase):
    def test_canonique_admise(self):                                        # FORMAT §1.1, §1.2
        t = '{"a":[1,-2,{"b":null}],"n":"é' + chr(0x2028) + '","z":true}'
        self.assertEqual(o.objet(ligne(t)), {"a": [1, -2, {"b": None}], "n": "é" + chr(0x2028), "z": True})

    def test_echappements_de_json(self):                                    # Q-R18-3
        admis = '{"s":"' + BS + '"' + BS + BS + BS + "n" + BS + 'u001f"}'
        self.assertEqual(o.objet(ligne(admis)), {"s": '"' + BS + chr(10) + chr(31)})
        for autre in ("u000a", "u00e9", "/", "u001F"):
            self.assertIsNone(o.objet(ligne('{"s":"' + BS + autre + '"}')), autre)

    def test_non_canonique(self):                                           # §1.2 : réécrire redonne les octets
        for t in ('{"a": 1}', '{"b":1,"a":2}', ' {"a":1}', '{"a":1} ', '{"a":1}' + chr(13), '{"a":1,"a":1}',
                  '{"a":-0}', '{"a":01}', '{"a":1.5}', '{"a":1e3}', '{"a":NaN}', '{"a":-Infinity}', "[1]", '"a"',
                  "1", "", "{}{}"):
            self.assertIsNone(o.objet(ligne(t)), t)
        self.assertIsNone(o.objet(b'{"a":1}'))                              # sans 0x0A final

    def test_octets_hors_utf8(self):                                        # §1.1 : UTF-8
        for brut in (b'{"a":"' + bytes((0xC3,)) + b'"}', b'{"a":"' + bytes((0xED, 0xA0, 0x80)) + b'"}',
                     ('{"a":"' + BS + 'ud800"}').encode(), bytes((0xEF, 0xBB, 0xBF)) + b'{"a":1}'):
            self.assertIsNone(o.objet(brut + NL), brut)

    def test_imbrication_excessive(self):                                   # §8.3 : RecursionError, non intègre
        self.assertIsNone(o.objet(ligne('{"a":' + "[" * 100000 + "]" * 100000 + "}")))

    def test_entiers_longs(self):                                           # Q-R18-2 ; E-R-01
        t = '{"a":' + "9" * 640 + ',"b":-1' + "0" * 639 + "}"
        self.assertEqual(o.objet(ligne(t)), {"a": 10 ** 640 - 1, "b": -(10 ** 639)})
        for t in ('{"a":' + "1" * 641 + "}", '{"a":-' + "1" * 641 + "}", '{"a":[' + "2" * 700 + "]}"):
            with self.assertRaises(o.RefusOracle) as r:
                o.objet(ligne(t))
            self.assertEqual(r.exception.code, "ORACLE/entier-long")
        for t in ('{"a":' + "1" * 641 + ',"b":1.5}', "[" + "1" * 641 + "]", '{"a":' + "1" * 641 + ",}"):
            self.assertIsNone(o.objet(ligne(t)), t[-9:])                    # non intègre d'abord

    def test_independant_du_reglage_de_l_interpreteur(self):                # PYTHONINTMAXSTRDIGITS, -X int_max…
        self.addCleanup(sys.set_int_max_str_digits, sys.get_int_max_str_digits())
        for reglage in (640, 0, 4300):
            sys.set_int_max_str_digits(reglage)
            self.assertEqual(o.objet(ligne('{"a":-' + "7" * 640 + "}")), {"a": -int("7" * 640)})
            self.assertRaises(o.RefusOracle, o.objet, ligne('{"a":' + "7" * 641 + "}"))


class Champs(unittest.TestCase):
    def test_champs_communs(self):                                          # FORMAT §1.3
        bon = {"type": "x", "seq": 3, "prec": PREC, "ws": 60}
        self.assertTrue(o.champs(bon))
        for k, v in (("type", 1), ("seq", True), ("seq", "3"), ("seq", None), ("prec", "AB" * 32),
                     ("prec", "ab" * 31), ("prec", PREC + "a"), ("prec", 0)):
            self.assertFalse(o.champs({**bon, k: v}), (k, v))
        for k in ("type", "seq", "prec"):
            self.assertFalse(o.champs({x: v for x, v in bon.items() if x != k}), k)


class Noms(unittest.TestCase):
    def test_grammaire_et_ordre(self):                                      # FORMAT §6.1, §7.2 ; Q-R18-5
        with tempfile.TemporaryDirectory() as d:
            for n in ("pool-2026-10-05-10.jsonl", "pool-2026-10-05-2.jsonl", "pool-2026-10-04-0.jsonl",
                      "pool-2026-10-05-0.jsonl", "pool-2026-10-05-01.jsonl", "pool.sha256", "pool.verrou",
                      "autre-2026-10-04-0.jsonl", "pool-2026-10-04-0.jsonl.bak", "pool-2026-1-04-0.jsonl",
                      "xpool-2026-10-04-0.jsonl", "pool-2026-10-04-0.json", "p.l-2026-10-04-0.jsonl",
                      "pxl-2026-10-04-0.jsonl"):
                open(os.path.join(d, n), "wb").close()
            self.assertEqual(o.fichiers(d, "pool"), ["pool-2026-10-04-0.jsonl", "pool-2026-10-05-0.jsonl",
                                                       "pool-2026-10-05-2.jsonl", "pool-2026-10-05-10.jsonl"])
            self.assertEqual(o.fichiers(d, "p.l"), ["p.l-2026-10-04-0.jsonl"])


class Frontiere(unittest.TestCase):
    def test_ni_lecteur_principal_ni_ecrivain(self):                        # l.539-540 : bibliothèque standard seule
        with open(o.__file__, "rb") as f:
            self.assertEqual(violations("shogen_s2bis", f.read()), [])
        code = "import sys, shogen_s2bis.recalc.oracle_indep; print(sorted(m for m in sys.modules if 'shogen' in m))"
        p = subprocess.run([sys.executable, "-B", "-c", code], cwd=RACINE, capture_output=True, timeout=60)
        self.assertEqual(p.stdout, b"['shogen_s2bis', 'shogen_s2bis.recalc', 'shogen_s2bis.recalc.oracle_indep']" + NL)
