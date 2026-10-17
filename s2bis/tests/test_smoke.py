"""CB-16 (E-C-37 ; PROPOSITION l.224, l.278 ; ADR-0029 l.81, l.222) : smoke sans prix, sur fixtures, sans réseau
(`lire` et `pause` remplacés). Lignes attendues écrites à la main ; prix interdits pris des fixtures par le décodeur
seul (jamais par le smoke) ; URL de CryptoCompare de S2 (`s2-harness/shogen_s2/sources.py` l.288-290)."""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

from shogen_s2bis.collecte import decodeurs, entree, http, smoke
from shogen_s2bis.collecte.lecture import Lecture
from tests.test_entree import configurations
from tests.test_secondaire import carte, fichiers

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
PIECES = {"binance_btc": "btc/binance.bin", "coinbase_eth": "actifs/coinbase_eth.bin",
          "binance_usdc": "actifs/binance_usdc.bin", "coingecko_groupe": "actifs/coingecko_groupe.bin",
          "chainlink_usdt": "actifs/chainlink_usdt.bin", "chainlink_eth": "actifs/chainlink_eth.bin",
          "okx_usdc_usdt": "temoin/okx_usdc_usdt.bin", "uniswap_usdc_usdt": "temoin/uniswap_usdc_usdt.bin",
          "curve_usdc_usdt": "temoin/curve_usdc_usdt.bin", "kraken_eth": "actifs/kraken_eth.bin"}
HOTES = {"binance_btc": "api.binance.com", "coinbase_eth": "api.exchange.coinbase.com", "binance_usdc":
         "api.binance.com", "coingecko_groupe": "api.coingecko.com", "chainlink_usdt": "ethereum-rpc.publicnode.com",
         "chainlink_eth": "ethereum-rpc.publicnode.com", "okx_usdc_usdt": "www.okx.com",
         "uniswap_usdc_usdt": "eth.drpc.org", "curve_usdc_usdt": "rpc.mevblocker.io", "kraken_eth": "api.kraken.com"}
ESPACE = ("api.binance.com", "api.exchange.coinbase.com", "www.okx.com")
TLS, POOL, CARTE = object(), 3_000_000, 7_000_000                  # délais distincts : chacun lu à sa source
CHAINLINK = {d: '{"jsonrpc": "2.0", "id": 1, "method": "eth_call", "params": [{"to": "%s", "data": "0xfeaf968c"}, '
             '"latest"]}' % a for d, a in (("chainlink_usdt", "0x3E7d1eAB13ad0104d2750B8863b489D65364e32D"),
                                           ("chainlink_eth", "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"))}


def forme(dec):                     # nom de forme ≠ nom du décodeur (site d'appel : le décodeur de la forme)
    corps = decodeurs.CORPS.get(dec, CHAINLINK.get(dec, ""))
    return {"nom": dec.replace("_", "-"), "hote": HOTES[dec], "port": 443, "chemin": "/" + dec, "methode":
            "POST" if corps else "GET", "corps": corps, "espace": HOTES[dec] in ESPACE, "decodeur": dec}


def lire(octets):
    with open(os.path.join(FIX, octets), "rb") as f:
        return f.read()


class Smoke(unittest.TestCase):
    def jouer(self, **servies):
        """(code, lignes, appels) : chaque forme servie par sa fixture (ou par `servies[décodeur]`, une Lecture), en
        123 ms ; CryptoCompare : `servies["cc"]`, 401 en 87 ms par défaut."""
        appels, lignes = [], []

        def faux(req, suivi, delai, tls):
            appels.append((req.hote, req.chemin, req.methode, req.corps, suivi, delai, tls is TLS))
            dec = req.chemin[1:]
            if req.hote == "min-api.cryptocompare.com":
                return servies.get("cc", Lecture("panne_http", 0, 87_000, code=401, octets=b'{"Response":"Error"}'))
            return servies.get(dec, Lecture("ok", 10 ** 15, 10 ** 15 + 123_456, code=200, octets=lire(PIECES[dec])))
        formes = [forme(d) for d in list(PIECES)[:-1]]
        code = smoke.jouer(formes, [forme("kraken_eth")], (POOL, CARTE), lire=faux,
                           pause=lambda s: appels.append(("pause", s)), tls=TLS, sortie=lignes.append)
        return code, lignes, appels

    def test_sortie_sans_aucun_prix_et_code_0_si_tout_decode(self):          # PROPOSITION l.278 (M : prix imprimé)
        code, lignes, _a = self.jouer()
        prix = [v["prix"] for d, p in PIECES.items() for v in decodeurs.decoder(d, lire(p))[1]]
        self.assertEqual(len(prix), 13)                             # garde : treize prix, décodés hors du smoke
        self.assertEqual([p for p in prix if p in "\n".join(lignes)], [])
        self.assertEqual((code, lignes), (0, [
            "pool binance-btc api.binance.com ok 200 - 123 ms décodable oui",
            "pool coinbase-eth api.exchange.coinbase.com ok 200 - 123 ms décodable oui",
            "pool binance-usdc api.binance.com ok 200 - 123 ms décodable oui",
            "pool coingecko-groupe api.coingecko.com ok 200 - 123 ms décodable oui",
            "pool chainlink-usdt ethereum-rpc.publicnode.com ok 200 - 123 ms décodable oui",
            "pool chainlink-eth ethereum-rpc.publicnode.com ok 200 - 123 ms décodable oui",
            "temoin okx-usdc-usdt www.okx.com ok 200 - 123 ms décodable oui",
            "temoin uniswap-usdc-usdt eth.drpc.org ok 200 - 123 ms décodable oui",
            "temoin curve-usdc-usdt rpc.mevblocker.io ok 200 - 123 ms décodable oui",
            "carte kraken-eth api.kraken.com ok 200 - 123 ms décodable oui",
            "exclue cryptocompare min-api.cryptocompare.com panne_http 401 - 87 ms attendu 401 : OK",
            "smoke : OK (9/9 formes du pool et du témoin décodées)"]))

    def test_code_1_si_une_forme_du_pool_ou_du_temoin_ne_decode_pas(self):
        """Pool illisible (200, corps vide d'objet) ou témoin en panne de transport : 1 ; carte en panne : déclarée,
        code 0 ; CryptoCompare en 200 ou 403 : écart déclaré, code inchangé."""
        illisible = Lecture("ok", 0, 5_000, code=200, octets=b"{}")
        delai = Lecture("panne_transport", 0, 10_000_000, sous_type="delai")
        cas = [({"binance_btc": illisible}, 1,
                "pool binance-btc api.binance.com panne_decode 200 - 5 ms décodable non"),
               ({"uniswap_usdc_usdt": delai}, 1,
                "temoin uniswap-usdc-usdt eth.drpc.org panne_transport - delai 10000 ms décodable non"),
               ({"kraken_eth": Lecture("panne_http", 0, 1_000, code=451)}, 0,
                "carte kraken-eth api.kraken.com panne_http 451 - 1 ms décodable non"),
               ({"cc": Lecture("ok", 0, 2_000, code=200, octets=b'{"USD":1}')}, 0,
                "exclue cryptocompare min-api.cryptocompare.com ok 200 - 2 ms attendu 401 : ÉCART"),
               ({"cc": Lecture("panne_http", 0, 2_000, code=403)}, 0,
                "exclue cryptocompare min-api.cryptocompare.com panne_http 403 - 2 ms attendu 401 : ÉCART")]
        for servies, attendu, ligne in cas:
            with self.subTest(ligne=ligne[:30]):
                code, lignes, _a = self.jouer(**servies)
                self.assertEqual((code, ligne in lignes, [x.split(" (")[0] for x in lignes[-1:]]),
                                 (attendu, True, ["smoke : ÉCHEC" if attendu else "smoke : OK"]))
        self.assertEqual(self.jouer(binance_btc=illisible, uniswap_usdc_usdt=delai)[1][-1:],
                         ["smoke : ÉCHEC (7/9 formes du pool et du témoin décodées)"])

    def test_requetes_delais_et_espacement(self):
        """Requête de chaque forme (méthode, corps du décodeur sur chaîne), suivi neuf, délai du pool ou de la carte,
        contexte TLS transmis ; une seconde de pause avant la seconde lecture de binance (espace vrai), aucune avant
        la seconde lecture de l'hôte de Chainlink (sans espace) ; CryptoCompare : GET de l'URL de S2, délai du pool."""
        _c, _l, appels = self.jouer()
        vus = [(a[0], a[1], a[2], a[5]) if a[0] != "pause" else a for a in appels]
        self.assertEqual(vus, [("api.binance.com", "/binance_btc", "GET", POOL),
                               ("api.exchange.coinbase.com", "/coinbase_eth", "GET", POOL), ("pause", 1),
                               ("api.binance.com", "/binance_usdc", "GET", POOL),
                               ("api.coingecko.com", "/coingecko_groupe", "GET", POOL),
                               ("ethereum-rpc.publicnode.com", "/chainlink_usdt", "POST", POOL),
                               ("ethereum-rpc.publicnode.com", "/chainlink_eth", "POST", POOL),
                               ("www.okx.com", "/okx_usdc_usdt", "GET", POOL), ("eth.drpc.org", "/uniswap_usdc_usdt",
                                                                                "POST", POOL),
                               ("rpc.mevblocker.io", "/curve_usdc_usdt", "POST", POOL),
                               ("api.kraken.com", "/kraken_eth", "GET", CARTE),
                               ("min-api.cryptocompare.com", "/data/price?fsym=BTC&tsyms=USD", "GET", POOL)])
        lus = [a for a in appels if a[0] != "pause"]
        self.assertEqual([(a[3], a[4], a[6]) for a in lus if a[0] == "rpc.mevblocker.io"],
                         [(decodeurs.CORPS["curve_usdc_usdt"].encode(), {}, True)])
        self.assertEqual({(a[3] is None) == (a[2] == "GET") and a[4] == {} and a[6] for a in lus}, {True})
        self.assertEqual(smoke.CRYPTOCOMPARE, http.Requete("min-api.cryptocompare.com",
                                                           "/data/price?fsym=BTC&tsyms=USD", 443, "GET", None))

    def test_role_par_la_classe_du_decodeur(self):                   # C-P2D-1 : classe `temoin`
        self.assertEqual([smoke.role({"decodeur": d}) for d in ("okx_usdc_usdt", "uniswap_usdc_usdt",
                                                                "curve_usdc_usdt", "okx_ticker_usdt", "chainlink_usdc",
                                                                "inconnu")],
                         ["temoin"] * 3 + ["pool"] * 3)


class Commande(unittest.TestCase):                                 # CB-16b ; FORMAT §18
    def test_commande_smoke_par_le_point_d_entree(self):
        """`smoke --formes F [--carte C]` : configurations contrôlées (schémas, règles, règles croisées) ; `http.lire`
        remplacé (aucun envoi), au délai de chaque fichier (pool 0,3 s, carte 0,25 s) ; sortie 0, puis 1 (témoin
        illisible) ; refus (carte hors de δ, fichier absent, décodeur inconnu de la carte puis du pool) : 2 et
        `smoke : refus : …`."""
        f, _s, _d = configurations(443)
        f["formes"], vus, illisible = [forme("binance_btc"), forme("okx_usdc_usdt")], [], []

        def faux(req, suivi, delai, tls):
            vus.append((req.hote, delai))
            if req.hote == "min-api.cryptocompare.com":
                return Lecture("panne_http", 0, 1_000, code=401)
            return Lecture("ok", 0, 2_000, code=200, octets=b"{}" if illisible else lire(PIECES[req.chemin[1:]]))

        def jouer(*args):
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = entree.main(["smoke", "--formes", ch["formes"], *args])
            return code, out.getvalue().splitlines(), err.getvalue()
        with tempfile.TemporaryDirectory() as t, mock.patch.object(smoke.http, "lire", side_effect=faux):
            ch = fichiers(t, formes=f, carte=carte(443, delai=250_000, formes=[forme("kraken_eth")]),
                          inconnu={**f, "formes": [{**forme("binance_btc"), "decodeur": "inconnu"}]},
                          large=carte(443, delai=350_001, formes=[forme("kraken_eth")]),
                          inconnue=carte(443, delai=250_000, formes=[{**forme("kraken_eth"), "decodeur": "inconnu"}]))
            ch["absente"] = os.path.join(t, "absente.json")
            r = [jouer("--carte", ch["carte"]), jouer()]
            illisible.append(1)
            r.append(jouer())
            refus = [jouer("--carte", ch[n])[::2] for n in ("large", "absente", "inconnue")]
            ch["formes"] = ch["inconnu"]
            refus.append(jouer()[::2])
        tete = ["pool binance-btc api.binance.com ok 200 - 2 ms décodable oui",
                "temoin okx-usdc-usdt www.okx.com ok 200 - 2 ms décodable oui"]
        fin = ["exclue cryptocompare min-api.cryptocompare.com panne_http 401 - 1 ms attendu 401 : OK",
               "smoke : OK (2/2 formes du pool et du témoin décodées)"]
        self.assertEqual(r[:2], [(0, tete + ["carte kraken-eth api.kraken.com ok 200 - 2 ms décodable oui"] + fin, ""),
                                 (0, tete + fin, "")])
        self.assertEqual((r[2][0], r[2][1][-1:]), (1, ["smoke : ÉCHEC (0/2 formes du pool et du témoin décodées)"]))
        self.assertEqual(vus[:4], [("api.binance.com", 300_000), ("www.okx.com", 300_000), ("api.kraken.com", 250_000),
                                   ("min-api.cryptocompare.com", 300_000)])
        self.assertEqual([(c, e[:16], e.strip().split(" : ")[2:]) for c, e in refus], [
            (2, "smoke : refus : ", ["CONFIG/incoherent", "hors-delta"]),
            (2, "smoke : refus : ", [f"[Errno 2] No such file or directory: {ch['absente']!r}"]),
            (2, "smoke : refus : ", ["CONFIG/incoherent", "decodeur-connu"]),
            (2, "smoke : refus : ", ["CONFIG/incoherent", "decodeur-connu"])])


if __name__ == "__main__":
    unittest.main()
