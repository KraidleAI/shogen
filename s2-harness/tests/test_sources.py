"""Tests déterministes des décodeurs — les typeurs de A(typer-correctness).

Deux familles :
  1. Régression sur fixtures live gelées (capture.py) : chaque décodeur relit
     les octets figés et doit rendre EXACTEMENT la valeur d'expected.json.
  2. Synthétiques ciblant chaque piège re-mesuré (10 §3.1) + le fail-closed :
     un corps illisible devient une panne, jamais une valeur inventée.

Stdlib seul (unittest) — zéro dépendance. Lancer : `python -m unittest -v`
depuis s2-harness/.
"""

from __future__ import annotations

import json
import os
import unittest

from shogen_s2 import sources
from shogen_s2.model import DecodeError
from shogen_s2.sources import SPECS

HERE = os.path.dirname(__file__)
FIX = os.path.join(HERE, "fixtures")
with open(os.path.join(HERE, "expected.json"), encoding="utf-8") as _f:
    EXPECTED = json.load(_f)
BY_ID = {s.flux_id: s for s in SPECS}


class TestFixtureRegression(unittest.TestCase):
    def test_each_decoder_matches_frozen_fixture(self):
        seen = 0
        for flux_id, exp in EXPECTED.items():
            if flux_id.startswith("_"):
                continue
            with self.subTest(flux=flux_id):
                with open(os.path.join(FIX, flux_id + ".bin"), "rb") as f:
                    raw = f.read()
                price, source_ts, extra = BY_ID[flux_id].decode(raw)
                self.assertEqual(str(price), exp["price"])
                self.assertEqual(source_ts, exp["source_ts"])
            seen += 1
        self.assertEqual(seen, 12, "les 12 flux doivent avoir une fixture")

    def test_cryptocompare_fixture_is_401(self):
        self.assertEqual(EXPECTED["_cryptocompare_http"], 401)


class TestFailClosed(unittest.TestCase):
    def test_garbage_body_is_panne_never_a_value(self):
        for flux_id, spec in BY_ID.items():
            with self.subTest(flux=flux_id):
                with self.assertRaises(Exception):
                    spec.decode(b"not json at all {[")

    def test_empty_body_is_panne(self):
        for flux_id, spec in BY_ID.items():
            with self.subTest(flux=flux_id):
                with self.assertRaises(Exception):
                    spec.decode(b"")


class TestQuirks(unittest.TestCase):
    """Chaque piège que la re-vérification aveugle (V2, 10 §3.1) a constaté."""

    def test_bitfinex_uses_index_6_not_last_element(self):
        # 11 champs (le piège : schéma documenté = 10) ; LAST_PRICE = index 6.
        raw = b"[1,2,3,4,5,6,64122,8,9,10,1358182043000]"
        price, ts, extra = sources._d_bitfinex(raw)
        self.assertEqual(str(price), "64122")

    def test_bitfinex_short_array_is_panne(self):
        with self.assertRaises(DecodeError):
            sources._d_bitfinex(b"[1,2,3]")

    def test_kraken_indexes_returned_key_not_requested_pair(self):
        raw = b'{"error":[],"result":{"XXBTZUSD":{"c":["64025.00","1.0"]}}}'
        price, ts, extra = sources._d_kraken(raw)
        self.assertEqual(str(price), "64025.00")

    def test_kraken_error_list_is_panne(self):
        with self.assertRaises(DecodeError):
            sources._d_kraken(b'{"error":["EQuery:Unknown"],"result":{}}')

    def test_chainlink_answer_is_word_2_updatedat_word_4(self):
        answer = 6403392226348          # 64033.92226348 à 8 décimales
        updated_at = 1785927743
        w = lambda x: f"{x:064x}"
        result = "0x" + w(7) + w(answer) + w(1785927700) + w(updated_at) + w(7)
        raw = json.dumps({"result": result}).encode()
        price, ts, extra = sources._d_chainlink(raw)
        self.assertEqual(str(price), "64033.92226348")
        self.assertEqual(ts, float(updated_at))
        self.assertEqual(extra["round_id"], "7")

    def test_chainlink_wrong_word_count_is_panne(self):
        with self.assertRaises(DecodeError):
            sources._d_chainlink(b'{"result":"0xabcd"}')

    def test_pyth_price_is_mantissa_times_ten_pow_expo(self):
        raw = json.dumps({"parsed": [{"price": {
            "price": "6400666876589", "conf": "1777126780",
            "expo": -8, "publish_time": 1785930190}}]}).encode()
        price, ts, extra = sources._d_pyth(raw)
        self.assertEqual(str(price), "64006.66876589")
        self.assertEqual(ts, 1785930190.0)


if __name__ == "__main__":
    unittest.main()
