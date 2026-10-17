"""CB-8c (SHOGEN-S2BIS-FORMES-BTC-1 ; E-C-09 ; ADR-0029 l.236) : formes de requête du pool, `config/formes-pool.json`,
une par lecture. Valeurs hors du code : URL et corps de S2 écrits à la main depuis `s2-harness/shogen_s2/sources.py`
(l.221-224, l.241-281), proxys Chainlink depuis la pièce (`docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md` §2 l.63-66),
lectures par hôte depuis la PROPOSITION du G0 de CALIB-ACTIFS (§2.2, l.170-172)."""
import collections
import json
import os
import unittest

from shogen_s2bis.collecte import boucle, config, decodeurs, entree, http
from shogen_s2bis.collecte.lecture import S

FORMES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "formes-pool.json")
REGLES = ("noms-uniques", "methode-corps", "hote-forme", "chemin-forme", "espace-par-hote", "decodeur-connu")
S2 = {"binance_btc": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",              # sources.py l.241-
      "coinbase_btc": "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
      "kraken_btc": "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
      "okx_ticker_btc": "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT",
      "okx_index_btc": "https://www.okx.com/api/v5/market/index-tickers?instId=BTC-USD",
      "bitstamp_btc": "https://www.bitstamp.net/api/v2/ticker/btcusd/",
      "gemini_btc": "https://api.gemini.com/v1/pubticker/btcusd",
      "chainlink_btc": "https://ethereum-rpc.publicnode.com"}         # l.223 : chemin vide, écrit « / »
CORPS_S2 = ('{"jsonrpc": "2.0", "id": 1, "method": "eth_call", "params": [{"to": "%s", "data": "0xfeaf968c"}, '
            '"latest"]}')                                    # json.dumps de post_body (sources.py l.62, l.278-281)
PROXYS = {"chainlink_btc": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c", "chainlink_eth":
          "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419", "chainlink_usdc": "0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6",
          "chainlink_usdt": "0x3E7d1eAB13ad0104d2750B8863b489D65364e32D"}

CHEMINS = {      # PROPOSITION du G0 de CALIB-ACTIFS §2.2 (l.159-168), préfixes des chemins de S2 pour l'hôte
    "binance_eth": "/api/v3/ticker/price?symbol=ETHUSDT", "binance_usdc": "/api/v3/ticker/price?symbol=USDCUSD",
    "binance_usdt": "/api/v3/ticker/price?symbol=USDTUSD", "coinbase_eth": "/products/ETH-USD/ticker",
    "coinbase_usdt": "/products/USDT-USD/ticker", "kraken_eth": "/0/public/Ticker?pair=ETHUSD",
    "kraken_usdc": "/0/public/Ticker?pair=USDCUSD", "kraken_usdt": "/0/public/Ticker?pair=USDTUSD",
    "okx_ticker_eth": "/api/v5/market/ticker?instId=ETH-USDT",
    "okx_ticker_usdt": "/api/v5/market/ticker?instId=USDT-USD", "bitstamp_eth": "/api/v2/ticker/ethusd/",
    "bitstamp_usdc": "/api/v2/ticker/usdcusd/", "bitstamp_usdt": "/api/v2/ticker/usdtusd/",
    "gemini_eth": "/v1/pubticker/ethusd", "gemini_usdc": "/v1/pubticker/usdcusd",
    "gemini_usdt": "/v1/pubticker/usdtusd",
    "bitfinex_groupe": "/v2/tickers?symbols=tBTCUSD,tETHUSD,tUDCUSD,tUSTUSD",
    "coingecko_groupe": "/api/v3/simple/price?ids=bitcoin,ethereum,usd-coin,tether&vs_currencies=usd"
                        "&include_last_updated_at=true",
    "defillama_groupe": "/prices/current/coingecko:bitcoin,coingecko:ethereum,coingecko:usd-coin,coingecko:tether",
    **{n: "/" for n in ("chainlink_eth", "chainlink_usdc", "chainlink_usdt")}}


def formes():
    return config.charger(FORMES, {"formes": [entree.FORME]}, [r for r in entree.COHERENCE["formes"]
                                                               if r[0] in REGLES])[0]["formes"]


class Formes(unittest.TestCase):
    def test_formes_controlees_requetes_construites(self):
        """Schéma et règles de forme de `formes.json` (FORMAT §14.1) ; chaque requête se construit (http.octets)."""
        f = formes()
        self.assertEqual(sorted(r[0] for r in entree.COHERENCE["formes"] if r[0] in REGLES), sorted(REGLES))
        self.assertEqual(len(f), 30)
        for x in f:
            with self.subTest(nom=x["nom"]):
                req = http.Requete(x["hote"], x["chemin"], x["port"], x["methode"], x["corps"].encode() or None)
                self.assertTrue(http.octets(req).startswith(f"{x['methode']} {x['chemin']} HTTP/1.1".encode()))

    def test_requete_btc_de_s2_gardee(self):                            # SHOGEN-S2BIS-FORMES-BTC-1
        """Huit flux BTC gardés : URL et corps de S2, octet pour octet (chemin vide de Chainlink écrit « / » par
        http.client, `putrequest` : « url = url or '/' », lu sous 3.10 à 3.13) ; CoinGecko, DefiLlama et Bitfinex
        regroupés (E-C-09) : aucune forme BTC seule pour eux."""
        f = {x["nom"]: x for x in formes()}
        self.assertEqual({n: ("https://" + f[n]["hote"] + f[n]["chemin"], f[n]["methode"], f[n]["corps"]) for n in S2
                          if n in f},
                         {n: (u + "/" * (u.count("/") == 2), "POST" if n in PROXYS else "GET", CORPS_S2 % PROXYS[n]
                              if n in PROXYS else "") for n, u in S2.items()})
        self.assertEqual(sorted(n for n in decodeurs.DECODEURS if n not in f),
                         ["bitfinex_btc", "coingecko_btc", "defillama_btc", "okx_usdc_usdt",
                          "uniswap_usdc_usdt"])                     # témoin (CB-9) : formes hors du pool
        self.assertEqual(sorted(x["decodeur"] for x in f.values()), sorted(f))      # décodeur = nom de la forme

    def test_chemins_des_paires_et_des_regroupements(self):          # CB-7, CB-8 : une forme par décodeur neuf
        f = {x["nom"]: x for x in formes()}
        self.assertEqual({n: x["chemin"] for n, x in f.items() if n not in S2}, CHEMINS)

    def test_chainlink_proxy_principal_par_actif(self):              # Q-CA-08 du G0 de CALIB-ACTIFS
        f = {x["nom"]: x for x in formes()}
        self.assertEqual({n: json.loads(f[n]["corps"])["params"][0]["to"] for n in PROXYS if n in f}, PROXYS)
        self.assertEqual([f[n]["corps"] for n in PROXYS if n in f], [CORPS_S2 % PROXYS[n] for n in PROXYS])

    def test_lectures_par_hote_et_budget(self):                     # E-C-09 ; AVIS Q-C-10 ; ADR-0029 l.236
        """Lectures par hôte et par fenêtre (PROPOSITION de CALIB-ACTIFS l.170-172) ; OKX à quatre, cinq avec le témoin
        `USDC-USDT` de CB-9 : plan de 0 à 4 s, budget 5 + 4 + 10 + 1 = 20 ≤ 20 s (tolérance, décalage, délai, marge)."""
        f = formes()
        self.assertEqual(collections.Counter(x["hote"] for x in f), {
            "api.binance.com": 4, "api.exchange.coinbase.com": 3, "api.kraken.com": 4, "www.okx.com": 4,
            "www.bitstamp.net": 4, "api.gemini.com": 4, "api-pub.bitfinex.com": 1, "api.coingecko.com": 1,
            "coins.llama.fi": 1, "ethereum-rpc.publicnode.com": 4})
        plan = boucle.planifier([(x["nom"], x["hote"]) for x in f] + [("temoin_okx", "www.okx.com")],
                                {x["hote"] for x in f if x["espace"]})
        self.assertEqual((plan[-1][0], 5 * S + plan[-1][0] + 10 * S + S <= 20 * S), (4 * S, True))
        with self.assertRaises(boucle.RefusBoucle):                 # une sixième forme d'OKX : regroupement (Q-C-10)
            boucle.planifier([(x["nom"], x["hote"]) for x in f] + [("a", "www.okx.com"), ("b", "www.okx.com")])


if __name__ == "__main__":
    unittest.main()
