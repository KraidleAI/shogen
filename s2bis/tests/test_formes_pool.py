"""CB-8c (SHOGEN-S2BIS-FORMES-BTC-1 ; E-C-09 ; ADR-0029 l.236) : formes de requête du pool, une par lecture. GEL-1 (gel
du collecteur ; Q-5 de P2C ; SHOGEN-S2BIS-CONFIG-PRODUCTION-1) : `config/formes.json` de production, formes de
`formes-pool.json` fondues dans leur ordre, paramètres de la boucle scellés, contrôlé par le schéma et toutes les règles
de `entree` ; chaque valeur scellée liée à sa ligne de l'ADR-0029 (convention du FORMAT : numéros au commit `e16956b`).
Valeurs hors du code : URL et corps de S2 écrits à la main depuis `s2-harness/shogen_s2/sources.py`
(l.221-224, l.241-281), proxys Chainlink depuis la pièce (`docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md` §2 l.63-66),
lectures par hôte depuis la PROPOSITION du G0 de CALIB-ACTIFS (§2.2, l.170-172)."""
import collections
import json
import os
import pathlib
import tempfile
import unittest

from shogen_s2bis.collecte import boucle, capture, config, decodeurs, entree, http
from shogen_s2bis.collecte.lecture import S

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORMES = os.path.join(RACINE, "config", "formes.json")
ADR = pathlib.Path(RACINE).parent / "docs" / "adr-0029" / "ADR-0029-campagne-S2-bis.md"
SCELLEES = {"w": 60,                    # ADR-0029 l.88 : « fenêtre j (w = 60 s, grille UTC »
            "delta": 20_000_000,        # l.233 : « δ = 20 s », en µs
            "delai": 10_000_000,        # l.233 : « délai 10 s par requête »
            "tolerance": 5_000_000,     # l.107, D-2 : « plus de 5 s après » (ajout daté du 2026-10-04 17:03:38 UTC)
            "marge": 1_000_000,         # l.233 : « échéance dure à ws + w − 1 s » ; budget « 5 + 10 + 1 ≤ 20 »
            "places": 40}               # décision de l'orchestrateur (brief du gel) : 33 formes, sept places de marge
PHRASES = ("w = 60 s", "δ = 20 s, délai 10 s par requête, échéance dure à ws + w − 1 s", "plus de 5 s après",
           "(5 + 4 + 10 + 1 = 20 ≤ 20 s)")                      # texte des lignes citées, cherché dans l'ADR
S2 = {"binance_btc": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",              # sources.py l.241-
      "coinbase_btc": "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
      "kraken_btc": "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
      "okx_ticker_btc": "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT",
      "okx_index_btc": "https://www.okx.com/api/v5/market/index-tickers?instId=BTC-USD",
      "bitstamp_btc": "https://www.bitstamp.net/api/v2/ticker/btcusd/",
      "gemini_btc": "https://api.gemini.com/v1/pubticker/btcusd",
      "chainlink_btc": "https://ethereum-rpc.publicnode.com"}         # l.223 : chemin vide, écrit « / »
BINANCE = "data-api.binance.vision"      # GEL-2 (Q-7 de P2C) : api.binance.com rend 451 (PAIRES-ET-TEMOIN l.37)
ECART = {"binance_btc": ("//api.binance.com/", "//" + BINANCE + "/")}   # écart à l'URL de S2 déclaré : hôte seul
CORPS_S2 = ('{"jsonrpc": "2.0", "id": 1, "method": "eth_call", "params": [{"to": "%s", "data": "0xfeaf968c"}, '
            '"latest"]}')                                    # json.dumps de post_body (sources.py l.62, l.278-281)
PROXYS = {"chainlink_btc": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c", "chainlink_eth":
          "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419", "chainlink_usdc": "0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6",
          "chainlink_usdt": "0x3E7d1eAB13ad0104d2750B8863b489D65364e32D"}

ORDRE = ["binance_btc", "coinbase_btc", "kraken_btc", "okx_ticker_btc", "okx_index_btc", "bitstamp_btc", "gemini_btc",
         "binance_usdc", "binance_usdt", "binance_eth", "coinbase_eth", "coinbase_usdt", "kraken_eth", "kraken_usdc",
         "kraken_usdt", "okx_ticker_usdt", "okx_ticker_eth", "bitstamp_eth", "bitstamp_usdc", "bitstamp_usdt",
         "gemini_eth", "gemini_usdc", "gemini_usdt", "bitfinex_groupe", "coingecko_groupe", "defillama_groupe",
         "chainlink_btc", "chainlink_eth", "chainlink_usdc", "chainlink_usdt", "okx_usdc_usdt", "uniswap_usdc_usdt",
         "curve_usdc_usdt"]                                    # formes-pool.json à la base 1d7e5d4, ligne par ligne

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
    **{n: "/" for n in ("chainlink_eth", "chainlink_usdc", "chainlink_usdt")},
    "okx_usdc_usdt": "/api/v5/market/ticker?instId=USDC-USDT", "uniswap_usdc_usdt": "/", "curve_usdc_usdt": "/"}


def formes():
    return config.charger(FORMES, entree.SCHEMAS["formes"], entree.COHERENCE["formes"])[0]["formes"]


class Formes(unittest.TestCase):
    def test_formes_controlees_requetes_construites(self):
        """Schéma et toutes les règles de `formes.json` (FORMAT §14.1), `formes-pool.json` fondu et supprimé (GEL-1) ;
        chaque requête se construit (http.octets)."""
        f = formes()
        self.assertEqual((len(f), os.path.exists(os.path.join(RACINE, "config", "formes-pool.json"))), (33, False))
        self.assertEqual([x["nom"] for x in f], ORDRE)               # ordre de `formes-pool.json` gardé (GEL-1)
        self.assertEqual(([x["nom"] for x in f if not capture.NOM.fullmatch(x["nom"])], "nom-forme" in dict(
            entree.COHERENCE["formes"])), ([], True))                 # GEL-3 : règle des noms (NOM-FORME-1)
        for x in f:
            with self.subTest(nom=x["nom"]):
                req = http.Requete(x["hote"], x["chemin"], x["port"], x["methode"], x["corps"].encode() or None)
                self.assertTrue(http.octets(req).startswith(f"{x['methode']} {x['chemin']} HTTP/1.1".encode()))

    def test_requete_btc_de_s2_gardee(self):                            # SHOGEN-S2BIS-FORMES-BTC-1
        """Huit flux BTC gardés : URL et corps de S2, octet pour octet (chemin vide de Chainlink écrit « / » par
        http.client, `putrequest` : « url = url or '/' », lu sous 3.10 à 3.13), hors de l'écart déclaré (ECART : hôte
        de Binance seul, GEL-2) ; CoinGecko, DefiLlama et Bitfinex regroupés (E-C-09) : aucune forme BTC seule pour eux.
        Les quatre formes de Binance sur `data-api.binance.vision` (Q-7 de P2C), chemins inchangés."""
        f = {x["nom"]: x for x in formes()}
        self.assertEqual({n: ("https://" + f[n]["hote"] + f[n]["chemin"], f[n]["methode"], f[n]["corps"]) for n in S2
                          if n in f},
                         {n: ((u + "/" * (u.count("/") == 2)).replace(*ECART.get(n, ("", ""))), "POST" if n in PROXYS
                              else "GET", CORPS_S2 % PROXYS[n] if n in PROXYS else "") for n, u in S2.items()})
        self.assertEqual({n: x["hote"] for n, x in f.items() if n.startswith("binance")}, dict.fromkeys(
            ("binance_btc", "binance_usdc", "binance_usdt", "binance_eth"), BINANCE))
        self.assertEqual(sorted(n for n in decodeurs.DECODEURS if n not in f),
                         ["bitfinex_btc", "coingecko_btc", "defillama_btc"])
        self.assertEqual(sorted(x["decodeur"] for x in f.values()), sorted(f))      # décodeur = nom de la forme

    def test_chemins_des_paires_et_des_regroupements(self):          # CB-7, CB-8 : une forme par décodeur neuf
        f = {x["nom"]: x for x in formes()}
        self.assertEqual({n: x["chemin"] for n, x in f.items() if n not in S2}, CHEMINS)

    def test_chainlink_proxy_principal_par_actif(self):              # Q-CA-08 du G0 de CALIB-ACTIFS
        f = {x["nom"]: x for x in formes()}
        self.assertEqual({n: json.loads(f[n]["corps"])["params"][0]["to"] for n in PROXYS if n in f}, PROXYS)
        self.assertEqual([f[n]["corps"] for n in PROXYS if n in f], [CORPS_S2 % PROXYS[n] for n in PROXYS])

    def test_lectures_par_hote_et_budget(self):                     # E-C-09 ; AVIS Q-C-10 ; ADR-0029 l.236
        """Lectures par hôte et par fenêtre (PROPOSITION de CALIB-ACTIFS l.170-172) ; OKX à cinq avec le témoin
        `USDC-USDT` (INT-P2-15) : plan de 0 à 4 s, budget 5 + 4 + 10 + 1 = 20 ≤ 20 s (tolérance, décalage, délai,
        marge) ; un hôte RPC par pièce du témoin (Q-CA-10)."""
        f = formes()
        self.assertEqual(collections.Counter(x["hote"] for x in f), {
            BINANCE: 4, "api.exchange.coinbase.com": 3, "api.kraken.com": 4, "www.okx.com": 5,
            "www.bitstamp.net": 4, "api.gemini.com": 4, "api-pub.bitfinex.com": 1, "api.coingecko.com": 1,
            "coins.llama.fi": 1, "ethereum-rpc.publicnode.com": 4, "eth.drpc.org": 1, "rpc.mevblocker.io": 1})
        plan = boucle.planifier([(x["nom"], x["hote"]) for x in f], {x["hote"] for x in f if x["espace"]})
        self.assertEqual((plan[-1][0], 5 * S + plan[-1][0] + 10 * S + S <= 20 * S), (4 * S, True))
        with self.assertRaises(boucle.RefusBoucle):                 # une sixième forme d'OKX : regroupement (Q-C-10)
            boucle.planifier([(x["nom"], x["hote"]) for x in f] + [("a", "www.okx.com")])

    def test_formes_du_temoin(self):                                # INT-P2-15 ; ADR-0029 l.174 ; Q-CA-10
        """Trois formes du témoin : OKX `USDC-USDT` (GET, espacé comme les autres lectures d'OKX), Uniswap sur
        `eth.drpc.org` et Curve sur `rpc.mevblocker.io` (POST du corps de leur décodeur, un seul lecteur par hôte)."""
        f = {x["nom"]: x for x in formes()}
        self.assertEqual({n: (f[n]["hote"], f[n]["methode"], f[n]["espace"], f[n]["corps"]) for n in (
            "okx_usdc_usdt", "uniswap_usdc_usdt", "curve_usdc_usdt") if n in f}, {
            "okx_usdc_usdt": ("www.okx.com", "GET", True, ""),
            "uniswap_usdc_usdt": ("eth.drpc.org", "POST", False, decodeurs.CORPS["uniswap_usdc_usdt"]),
            "curve_usdc_usdt": ("rpc.mevblocker.io", "POST", False, decodeurs.CORPS["curve_usdc_usdt"])})

    def test_valeurs_scellees_liees_a_l_adr(self):                  # GEL-1 ; SHOGEN-S2BIS-CONFIG-PRODUCTION-1
        """Paramètres de la boucle égaux aux constantes écrites ici, chacune sous sa ligne de l'ADR ; le texte de ces
        lignes figure à l'ADR ; budget à l'égalité (5 + 4 + 10 + 1 = 20 s) ; `entree.configurer` admet le fichier."""
        f = config.charger(FORMES, entree.SCHEMAS["formes"], entree.COHERENCE["formes"])[0]
        self.assertEqual({k: f[k] for k in SCELLEES}, SCELLEES)
        texte = " ".join(ADR.read_text(encoding="utf-8").split())
        self.assertEqual([p for p in PHRASES if p not in texte], [])
        plan = boucle.planifier([(x["nom"], x["hote"]) for x in f["formes"]], {x["hote"] for x in f["formes"] if
                                                                                x["espace"]})
        self.assertEqual((f["tolerance"] + plan[-1][0] + f["delai"] + f["marge"], f["places"] - len(f["formes"])),
                         (f["delta"], 7))
        sante = {"commande": ["chronyc", "-n", "tracking"], "temoins": ["127.0.9.1"], "noms": ["a.example."],
                 "delai": 2 * S}
        descripteur = {"observateur": "o1", "fournisseur": "essai", "region": "essai", "asn": 64512, "resolveur":
                       "127.0.9.53", "config_resolveur": "resolv.conf", "versions": ["python3"], "empreinte": "e" * 64}
        with tempfile.TemporaryDirectory() as d:
            chemins = {"formes": FORMES}
            for nom, x in (("sante", sante), ("descripteur", descripteur)):
                chemins[nom] = os.path.join(d, nom + ".json")
                pathlib.Path(chemins[nom]).write_text(json.dumps(x), encoding="utf-8")
            self.assertEqual(entree.configurer(chemins, "0" * 40)["formes"][0], f)


if __name__ == "__main__":
    unittest.main()
