"""CB-7a (SHOGEN-S2BIS-DECODEURS-TYPES-1) : un conteneur remplacé ne rend jamais une autre valeur, à chaque décodeur
qui a une fixture (BTC compris).
CB-7b (E-C-06, E-C-08 ; ADR-0029 l.173 ; G0 de CALIB-ACTIFS, PROPOSITION §2.2 adoptée par l'avis) : décodeurs ETH, USDC
et USDT des places, un par (hôte, actif), sur les paires servies lues sur pièce
(`docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md`, tableau 1.1). Fixtures écrites octet pour octet depuis les formes de
réponse de la pièce (tableau 1.2), valeurs mesurées du tableau 1.1, champs élidés construits (rapport du lot) ; valeurs
attendues écrites à la main depuis la pièce, instants par date -u -d. CB-7c, CB-8a, CB-8b : même méthode."""
import json
import os
import unittest
from decimal import Decimal

from shogen_s2bis.collecte import decodeurs

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX, BTC = (os.path.join(RACINE, "tests", "fixtures", d) for d in ("actifs", "btc"))
PANNE = ("panne_decode", None)
H, P = "place_horodatee", "sans_horodatage"
# nom : (actif, classe, devise, préfixe du prix dans la fixture, prix, instant en µs)
PLACES = {"binance_usdc": ("USDC", P, "USD", b'"price":', "0.99996000", None),                  # pièce l.23
          "binance_usdt": ("USDT", P, "USD", b'"price":', "0.99933000", None),
          # 2026-10-08T19:29:04Z = 1791487744 (date -u -d), fraction de 9 chiffres tronquée ; pièce l.45
          "coinbase_eth": ("ETH", H, "USD", b'"price":', "2454.47", 1791487744979476),
          "coinbase_usdt": ("USDT", H, "USD", b'"price":', "0.9992", 1791487746512000),          # 19:29:06Z
          "kraken_eth": ("ETH", P, "USD", b'"c":[', "2454.74000", None),                          # pièce l.25
          "kraken_usdc": ("USDC", P, "USD", b'"c":[', "0.99990000", None),
          "kraken_usdt": ("USDT", P, "USD", b'"c":[', "0.99921000", None),
          # ts 1791487760072 = 19:29:20.072Z (pièce l.47, date -u -d)
          "okx_ticker_usdt": ("USDT", H, "USD", b'"last":', "0.99939", 1791487760072000),
          "bitstamp_eth": ("ETH", H, "USD", b'"last":', "2455.08", 1791487745000000),            # 19:29:05Z
          "bitstamp_usdc": ("USDC", H, "USD", b'"last":', "0.99976", 1791487746000000),
          "bitstamp_usdt": ("USDT", H, "USD", b'"last":', "0.99919", 1791487747000000),
          # volume.timestamp 1791487740000 = 19:29:00Z (pièce l.49)
          "gemini_eth": ("ETH", H, "USD", b'"last":', "2454.44000", 1791487740000000),
          "gemini_usdc": ("USDC", H, "USD", b'"last":', "0.99982", 1791487740000000),
          "gemini_usdt": ("USDT", H, "USD", b'"last":', "0.99918", 1791487740000000)}


def lire(*chemin):
    with open(os.path.join(*chemin), "rb") as f:
        return f.read()


def fixtures():
    """{décodeur : octets} : fixtures de CB-7 et CB-8 (`actifs/`), puis celles de BTC (`btc/<flux>.bin`)."""
    f = {n[:-4]: lire(FIX, n) for n in os.listdir(FIX)}
    return {**f, **{n[:-4] + "_btc": lire(BTC, n) for n in os.listdir(BTC)}}


def texte(x):
    """JSON compact, nombres écrits par leur texte Decimal (comme lus)."""
    if type(x) is dict:
        return "{" + ",".join(json.dumps(k) + ":" + texte(v) for k, v in x.items()) + "}"
    if type(x) is list:
        return "[" + ",".join(map(texte, x)) + "]"
    return str(x) if type(x) is Decimal else json.dumps(x)


def remplacements(x):
    """Variantes de x où un conteneur (racine comprise) est remplacé par son texte JSON, par l'autre sorte de
    conteneur (objet en liste de ses valeurs, liste en objet) ou par l'un de ses enfants scalaires (Kraken `c` en
    « 64025.00 »)."""
    if type(x) not in (dict, list):
        return
    enfants = list(x.values()) if type(x) is dict else x
    yield texte(x)
    yield enfants if type(x) is dict else {str(i): v for i, v in enumerate(x)}
    yield from (v for v in enfants if type(v) not in (dict, list))
    for k in (x if type(x) is dict else range(len(x))):
        for v in remplacements(x[k]):
            yield {**x, k: v} if type(x) is dict else x[:k] + [v] + x[k + 1:]


class Places(unittest.TestCase):
    def test_paires_servies_valeurs_des_fixtures(self):
        """Actif, classe de S2 pour l'hôte (`sources.py` l.305-313), devise de la paire, prix et instant de la pièce."""
        for nom, (actif, classe, devise, _champ, prix, ts) in PLACES.items():
            with self.subTest(nom=nom):
                self.assertEqual(decodeurs.decoder(nom, lire(FIX, nom + ".bin")), ("ok", [
                    {"actif": actif, "classe": classe, "devise": devise, "extra": {}, "prix": prix, "ts_source": ts}]))
        # le champ du prix d'OKX est un paramètre de la forme ; dans la fixture, `bidPx` égale `last` (pièce l.47) :
        # corps où chaque champ de prix diffère des autres (garde : six valeurs distinctes)
        prix_okx = {"last": "1.1", "bidPx": "1.2", "askPx": "1.3", "idxPx": "1.4", "open24h": "1.5", "sodUtc0": "1.6"}
        corps = json.dumps({"code": "0", "data": [{"instId": "USDT-USD", **prix_okx, "ts": "1791487760072"}]})
        r = decodeurs.decoder("okx_ticker_usdt", corps.encode())
        self.assertEqual((len(set(prix_okx.values())), [x["prix"] for x in r[1] or []]), (6, ["1.1"]))

    def test_prix_non_fini_nul_ou_negatif_a_chaque_place(self):                # E-C-06
        for nom, (*_a, avant, prix, _t) in PLACES.items():
            for p in (b'"NaN"', b'"0"', b'"-1"', b'"1E+1000000"'):
                corps = lire(FIX, nom + ".bin").replace(avant + b'"' + prix.encode() + b'"', avant + p)
                with self.subTest(nom=nom, prix=p):
                    self.assertEqual((corps.count(avant + p), decodeurs.decoder(nom, corps)), (1, PANNE))

    def test_instrument_rendu_exige(self):
        """Binance `symbol`, Kraken clé rendue, OKX `instId` : la réponse d'une autre paire est une panne."""
        for nom, autre in (("binance_usdc", "binance_usdt"), ("binance_usdt", "binance_usdc"), ("kraken_eth",
                           "kraken_usdc"), ("kraken_usdc", "kraken_usdt"), ("kraken_usdt", "kraken_eth")):
            with self.subTest(nom=nom):
                self.assertEqual(decodeurs.decoder(nom, lire(FIX, autre + ".bin")), PANNE)
        self.assertEqual(decodeurs.decoder("okx_ticker_usdt", lire(BTC, "okx_ticker.bin")), PANNE)

    def test_paires_absentes_sans_decodeur(self):
        """Coinbase USDC/USD, OKX ETH/USD et USDC/USD ne sont pas servies (pièce l.24, l.26) : aucun décodeur."""
        self.assertEqual([n for n, (a, d, _c, _l) in decodeurs.DECODEURS.items() if n.startswith("coinbase") and
                          a == "USDC" or n.startswith("okx") and (a == "USDC" or (a, d) == ("ETH", "USD"))], [])



class Types(unittest.TestCase):                                   # SHOGEN-S2BIS-DECODEURS-TYPES-1
    def test_conteneur_remplace_jamais_une_autre_valeur(self):
        """Chaque conteneur de chaque fixture remplacé (texte, autre conteneur, enfant scalaire) : `panne_decode` ou la
        même valeur, jamais une autre (S2 : Kraken `c` en chaîne rendait « 6 »)."""
        for nom, corps in sorted(fixtures().items()):
            base = json.loads(corps, parse_float=Decimal, parse_int=Decimal)
            attendu = decodeurs.decoder(nom, texte(base).encode())
            self.assertEqual(attendu[0], "ok", nom)
            with self.subTest(nom=nom):
                self.assertEqual([v for v in map(texte, remplacements(base)) if decodeurs.decoder(nom, v.encode()) not
                                  in (PANNE, attendu)], [])
        self.assertEqual(decodeurs.decoder("kraken_btc", b'{"error":[],"result":{"XXBTZUSD":{"c":"64025.00"}}}'),
                         PANNE)


if __name__ == "__main__":
    unittest.main()
