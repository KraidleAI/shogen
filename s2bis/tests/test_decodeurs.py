"""CB-6a (E-C-06, E-C-08 ; ADR-0029 l.231 ; PROPOSITION §2.4) : décodeurs BTC repris de S2. Valeurs hors du code :
`s2-harness/tests/expected.json` (capturé et décodé par S2), lu en Decimal depuis son texte ; fixtures copiées octet
pour octet ; classes de S2 (`sources.py` l.305-313) ; instants par date -u -d, 2^53 par bc (journal G1)."""
import hashlib
import json
import os
import unittest
from decimal import Decimal

from shogen_s2bis.collecte import decodeurs

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S2, FIX = os.path.join(os.path.dirname(RACINE), "s2-harness", "tests"), os.path.join(RACINE, "tests", "fixtures", "btc")
FLUX = {"binance": "sans_horodatage", "coinbase": "place_horodatee", "kraken": "sans_horodatage",
        "okx_ticker": "place_horodatee", "okx_index": "place_horodatee", "bitstamp": "place_horodatee",
        "gemini": "place_horodatee", "bitfinex": "sans_horodatage"}
PANNE = ("panne_decode", None)


def lire(*chemin):
    with open(os.path.join(*chemin), "rb") as f:
        return f.read()


def prix(nom, corps):                                             # (prix, instant) du relevé unique, ou le statut
    statut, valeurs = decodeurs.decoder(nom, corps)
    return (valeurs[0]["prix"], valeurs[0]["ts_source"]) if statut == "ok" else statut


class Reprise(unittest.TestCase):
    def test_fixtures_copiees_octet_pour_octet(self):
        self.assertEqual(sorted(os.listdir(FIX)), sorted(f + ".bin" for f in FLUX))
        for f in FLUX:
            with self.subTest(flux=f):
                self.assertEqual(hashlib.sha256(lire(FIX, f + ".bin")).digest(),
                                 hashlib.sha256(lire(S2, "fixtures", f + ".bin")).digest())

    def test_memes_valeurs_que_expected_json_de_s2(self):
        """Un relevé par fixture : prix de S2 à la lettre, instant de S2 (secondes) en microsecondes exactes, devise,
        extra ; classe de S2 ; « sans horodatage » si et seulement si aucun instant (concordance de S2, l.301-304)."""
        attendu = json.loads(lire(S2, "expected.json"), parse_float=Decimal)
        self.assertEqual(sorted(decodeurs.DECODEURS), sorted(f + "_btc" for f in FLUX))
        for f, classe in FLUX.items():
            e = attendu[f]
            ts = None if e["source_ts"] is None else int(e["source_ts"] * 10 ** 6)
            with self.subTest(flux=f):
                self.assertEqual((classe == "sans_horodatage") == (ts is None), True)
                self.assertEqual(decodeurs.decoder(f + "_btc", lire(FIX, f + ".bin")), ("ok", [
                    {"actif": "BTC", "classe": classe, "devise": e["currency"], "extra": e["extra"], "prix": e["price"],
                     "ts_source": ts}]))
        # écrit à la main : 2026-08-05T16:11:21Z = 1785946281 (date -u -d), fraction de 9 chiffres tronquée comme en S2
        self.assertEqual(prix("coinbase_btc", lire(FIX, "coinbase.bin")), ("64475.75", 1785946281674372))


class Pieges(unittest.TestCase):                                  # S2, tests/test_sources.py, TestQuirks
    def test_bitfinex_position_6_jamais_le_dernier(self):
        self.assertEqual(prix("bitfinex_btc", b"[1,2,3,4,5,6,64122,8,9,10,1358182043000]"), ("64122", None))
        self.assertEqual(decodeurs.decoder("bitfinex_btc", b"[1,2,3,4,5,6,7,8,9]"), PANNE)     # moins de 10 champs

    def test_kraken_cle_rendue_liste_d_erreurs(self):
        self.assertEqual(prix("kraken_btc", b'{"error":[],"result":{"XXBTZUSD":{"c":["64025.00","1.0"]}}}'),
                         ("64025.00", None))
        for corps in (b'{"error":["EQuery:Unknown"],"result":{"X":{"c":["1"]}}}', b'[]',
                      b'{"error":[],"result":{"A":{"c":["1"]},"B":{"c":["1"]}}}'):
            self.assertEqual(decodeurs.decoder("kraken_btc", corps), PANNE)


class Finitude(unittest.TestCase):                               # E-C-06 ; analogue de SHOGEN-PRIX-NON-FINI-1
    def test_prix_non_fini_nul_negatif_ou_flottant_panne(self):
        for p in ('"NaN"', '"sNaN"', '"Infinity"', '"-Infinity"', "NaN", "Infinity", '"0"', "0", "-0", '"0E-8"',
                  '"-1"', '"1E+1000000"', '"1E-1000000"', "true", "null", '["1"]', '"x"'):
            with self.subTest(prix=p):
                self.assertEqual(decodeurs.decoder("binance_btc", ('{"price":' + p + "}").encode()), PANNE)
        for p, attendu in (('"1E+999999"', "1E+999999"), ('"1E-999999"', "1E-999999"), ("64529.5", "64529.5")):
            self.assertEqual(prix("binance_btc", ('{"price":' + p + "}").encode()), (attendu, None))

    def test_instant_de_0_a_2_puissance_53_microsecondes(self):
        """2^53 = 9007199254740992 (bc) : instant de la source en microsecondes, de 0 inclus à 2^53 exclu."""
        def okx(ts, code="0"):
            return prix("okx_ticker_btc", ('{"code":"' + code + '","data":[{"last":"1","ts":"' + ts + '"}]}').encode())
        self.assertEqual([okx("9007199254740"), okx("9007199254741"), okx("0"), okx("-1"), okx("0", "51001")],
                         [("1", 9007199254740000), "panne_decode", ("1", 0), "panne_decode", "panne_decode"])

    def test_horodatage_iso_meme_lecture_de_3_10_a_3_13(self):
        """Fraction de 0 à 9 chiffres, décalage « ±HH:MM » ou « Z », instant sans décalage lu en UTC ; tout le reste
        est une panne, sous chaque version (fromisoformat de 3.10 refuse une fraction de 4 chiffres, 3.11 l'admet)."""
        def coinbase(t):
            return prix("coinbase_btc", json.dumps({"price": "1", "time": t}).encode())
        cas = [("2026-08-05T16:11:21Z", ("1", 1785946281000000)),
               ("2026-08-05T16:11:21.6743Z", ("1", 1785946281674300)),
               ("2026-08-05T18:11:21.674372+02:00", ("1", 1785946281674372)),
               ("2026-08-05T16:11:21.674372", ("1", 1785946281674372)), ("2026-08-05 16:11:21Z", "panne_decode"),
               ("2026-08-05T16:11:21+0000", "panne_decode"), ("1969-12-31T23:59:59Z", "panne_decode"),
               ("2255-06-05T23:47:34.740991Z", ("1", (1 << 53) - 1)), ("2255-06-05T23:47:34.740992Z", "panne_decode")]
        self.assertEqual([coinbase(t) for t, _a in cas], [a for _t, a in cas])     # 2^53 µs : 2255-06-05T23:47:34Z


class Illisible(unittest.TestCase):
    def test_corps_illisible_vide_profond_ou_nom_inconnu_panne_jamais_une_valeur(self):
        for nom in decodeurs.DECODEURS:
            for corps in (b"not json at all {[", b"", b"[" * 100000, b'"' + bytes([0xFF]) + b'"'):
                with self.subTest(nom=nom, corps=corps[:8]):
                    self.assertEqual(decodeurs.decoder(nom, corps), PANNE)
        self.assertEqual(decodeurs.decoder("inconnu", lire(FIX, "binance.bin")), PANNE)


if __name__ == "__main__":
    unittest.main()
