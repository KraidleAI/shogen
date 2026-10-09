"""Lecteurs de bougies et normalisation (T-CA-FMT-1 à 3 ; E-CA-16), sur octets synthétiques écrits à la main
(1775001600 = 2026-04-01 00:00 UTC, date -u -d). Chaque test nomme la mutation qui le rougit."""
import io
import json
import unittest
import zipfile
from decimal import Decimal

import bougies
import socle

T0, FEN = 1775001600, {"debut": 1775001600, "fin": 1775001600 + 600}


def zipper(texte, membres=1):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        for i in range(membres):
            z.writestr(f"m{i}.csv", texte)
    return b.getvalue()


def binance(temps, cloture="1.5", volume="10"):
    return ",".join([temps, "1", "2", "0.5", cloture, volume, "0", "0", "0", "0", "0", "0"]) + bougies.NL


class TestBougies(unittest.TestCase):
    def assertRefus(self, format_, fichiers, fen=FEN):
        with self.assertRaises(socle.Refus) as r:
            bougies.serie(format_, fichiers, fen, "p", "ETH")
        self.assertEqual((r.exception.code, "place p" in str(r.exception)), ("CA/format", True))

    def test_binance_unites(self):
        """T-CA-FMT-1 : 1775001600000000 µs et 1775001600000 ms donnent la même minute ; clôture en colonne 4 (1,5,
        distincte de l'ouverture 1, du haut 2, du bas 0,5). Mutation M-CA-05 : microsecondes lues en millisecondes."""
        for temps in ("1775001600000000", "1775001600000"):
            self.assertEqual(bougies.serie("binance", [zipper(binance(temps))], FEN), {T0: (Decimal("1.5"), True)})
        self.assertRefus("binance", [zipper(binance("1775001600000500"))])
        self.assertRefus("binance", [zipper(binance("1775001600000"), membres=2)])

    def test_colonnes(self):
        """T-CA-FMT-2 : Bitfinex [MTS, OPEN, CLOSE, HIGH, LOW, VOLUME] : clôture en colonne 2 ; Coinbase [time, low,
        high, open, close, volume] : en colonne 4 ; nombres JSON lus en chaînes, jamais en flottant (0.1 exact) ; OKX
        par noms d'en-tête. Mutations M-CA-06 : colonne de Coinbase prise pour Bitfinex ; nombre JSON lu en flottant."""
        bf = json.dumps([[T0 * 1000, 1, 0.1, 2, 0.5, 3]]).encode()
        cb = json.dumps([[T0 + 60, 0.5, 2, 1, 0.1, 3]]).encode()
        okx = zipper("instrument_name,open,high,low,close,vol,vol_ccy,vol_quote,open_time,confirm" + bougies.NL
                     + f"ETH-USDT,1,2,0.5,0.1,3,0,0,{(T0 + 120) * 1000},1" + bougies.NL)
        self.assertEqual([bougies.serie(f, [o], FEN) for f, o in (("bitfinex", bf), ("coinbase", cb), ("okx", okx))],
                         [{T0: (Decimal("0.1"), True)}, {T0 + 60: (Decimal("0.1"), True)},
                          {T0 + 120: (Decimal("0.1"), True)}])

    def test_minutes_sans_echange(self):
        """T-CA-FMT-3 : minute absente chez Kraken (T0 + 60) : hors série ; minute reportée à volume 0 chez Bitstamp :
        non active. Mutation M-CA-07 : minute reportée comptée active."""
        kr = f"{T0},1,2,0.5,1.5,4,2{bougies.NL}{T0 + 120},1,2,0.5,1.6,1,1{bougies.NL}".encode()
        self.assertEqual(sorted(bougies.serie("kraken", [kr], FEN)), [T0, T0 + 120])
        bs = json.dumps({"data": {"pair": "ETH/USD", "ohlc": [
            {"timestamp": str(T0), "open": "1", "high": "1", "low": "1", "close": "1.5", "volume": "0.20000000"},
            {"timestamp": str(T0 + 60), "open": "1.5", "high": "1.5", "low": "1.5", "close": "1.5",
             "volume": "0.00000000"}]}}).encode()
        self.assertEqual(bougies.serie("bitstamp", [bs], FEN), {T0: (Decimal("1.5"), True),
                                                              T0 + 60: (Decimal("1.5"), False)})

    def test_refus(self):
        """CA/format : temps hors fenêtre (borne haute exclue), hors minute, minute en double (dans deux fichiers),
        Kraken à 6 colonnes, clôture NaN ou infinie, volume négatif, corps JSON d'erreur. Mutations : borne haute
        incluse ; double admis ; contrôle de finitude retiré."""
        k = "{},1,2,0.5,{},{},1" + bougies.NL
        for fichiers in ([k.format(T0 + 600, 1, 1)], [k.format(T0 + 30, 1, 1)], [k.format(T0, 1, 1)] * 2,
                         [k.format(T0, 1, 1).replace(",1" + bougies.NL, bougies.NL)], [k.format(T0, "NaN", 1)],
                         [k.format(T0, "Infinity", 1)], [k.format(T0, 1, -1)]):
            self.assertRefus("kraken", [x.encode() for x in fichiers])
        self.assertRefus("coinbase", [b'{"message": "NotFound"}'])


if __name__ == "__main__":
    unittest.main()
