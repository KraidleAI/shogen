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
from unittest import mock

from shogen_s2bis.collecte import decodeurs

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX, BTC = (os.path.join(RACINE, "tests", "fixtures", d) for d in ("actifs", "btc"))
PANNE = ("panne_decode", None)
H, P = "place_horodatee", "sans_horodatage"
# nom : (actif, classe, devise, préfixe du prix dans la fixture, prix, instant en µs)
PLACES = {"binance_usdc": ("USDC", P, "USD", b'"price":', "0.99996000", None),                  # pièce l.23
          "binance_usdt": ("USDT", P, "USD", b'"price":', "0.99933000", None),
          "binance_eth": ("ETH", P, "USDT", b'"price":', "2455.94000000", None),        # CB-7c, Q-CA-01 (a) ; l.23
          # 2026-10-08T19:29:04Z = 1791487744 (date -u -d), fraction de 9 chiffres tronquée ; pièce l.45
          "coinbase_eth": ("ETH", H, "USD", b'"price":', "2454.47", 1791487744979476),
          "coinbase_usdt": ("USDT", H, "USD", b'"price":', "0.9992", 1791487746512000),          # 19:29:06Z
          "kraken_eth": ("ETH", P, "USD", b'"c":[', "2454.74000", None),                          # pièce l.25
          "kraken_usdc": ("USDC", P, "USD", b'"c":[', "0.99990000", None),
          "kraken_usdt": ("USDT", P, "USD", b'"c":[', "0.99921000", None),
          # ts 1791487760072 = 19:29:20.072Z (pièce l.47, date -u -d)
          "okx_ticker_usdt": ("USDT", H, "USD", b'"last":', "0.99939", 1791487760072000),
          "okx_ticker_eth": ("ETH", H, "USDT", b'"last":', "2455.7", 1791487760101000),    # CB-7c ; l.26, ts construit
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
        self.assertEqual([decodeurs.decoder(n, lire(FIX, a + ".bin")) for n, a in (("binance_eth", "binance_usdt"), (
            "okx_ticker_eth", "okx_ticker_usdt"), ("okx_ticker_usdt", "okx_ticker_eth"))], [PANNE] * 3)     # CB-7c

    def test_paires_absentes_sans_decodeur(self):
        """Coinbase USDC/USD, OKX ETH/USD et USDC/USD ne sont pas servies (pièce l.24, l.26) : aucun décodeur."""
        self.assertEqual([n for n, (a, d, _c, _l) in decodeurs.DECODEURS.items() if n.startswith("coinbase") and
                          a == "USDC" or n.startswith("okx") and (a == "USDC" or (a, d) == ("ETH", "USD"))], [])


    def test_eth_cote_en_usdt_chez_binance_et_okx(self):                # CB-7c
        """Q-CA-01 (a) du G0 de CALIB-ACTIFS (avis l.41, adopté) : binance `ETHUSDT` et okx `ETH-USDT`, cotés en USDT
        comme pour BTC (ADR-0029 l.98) ; aucun ETH de ces deux hôtes coté en USD."""
        self.assertEqual(sorted((n, a, d) for n, (a, d, _c, _l) in decodeurs.DECODEURS.items() if a == "ETH" and
                                n.startswith(("binance", "okx"))), [("binance_eth", "ETH", "USDT"),
                                                                     ("okx_ticker_eth", "ETH", "USDT")])


def releves(classe, *lignes):
    return ("ok", [{"actif": a, "classe": classe, "devise": "USD", "extra": x, "prix": p, "ts_source": t}
                   for a, p, t, x in lignes])


def groupe(*releves_rendus, actif=None, devise="USD", classe="agregateur"):
    """Décodeur regroupé injecté, qui rend `releves_rendus` [(actif, prix, ts, extra)] quel que soit le corps."""
    return mock.patch.dict(decodeurs.DECODEURS, g=(actif, devise, classe, lambda j: list(releves_rendus)))


class Groupes(unittest.TestCase):             # CB-8a : lectures regroupées (E-C-09 ; ADR-0029 l.236 ; FORMAT §9.1)
    def test_coingecko_regroupe_quatre_releves(self):              # PROPOSITION du G0 de collecte l.263
        """Une lecture, quatre relevés, dans l'ordre BTC, ETH, USDC, USDT ; instants par actif (pièce l.51 :
        1791488055 = 19:34:15Z, 1791488110 = 19:35:10Z, date -u -d) ; BTC repris de la fixture de S2."""
        self.assertEqual(decodeurs.decoder("coingecko_groupe", lire(FIX, "coingecko_groupe.bin")), releves(
            "agregateur", ("BTC", "64432", 1785946180000000, {}), ("ETH", "2456.08", 1791488055000000, {}),
            ("USDC", "0.999622", 1791488110000000, {}), ("USDT", "0.999319", 1791488055000000, {})))

    def test_defillama_regroupe_quatre_releves(self):
        c = {"confidence": "0.99"}                                  # pièce l.52 : 1791487701 = 19:28:21Z
        self.assertEqual(decodeurs.decoder("defillama_groupe", lire(FIX, "defillama_groupe.bin")), releves(
            "agregateur", ("BTC", "64436.511163191906", 1785946190000000, c), ("ETH", "2455.7712345",
                                                                                1791487701000000, c),
            ("USDC", "0.99963", 1791487702000000, c), ("USDT", "0.9993", 1791487703000000, c)))

    def test_bitfinex_regroupe_positions_des_champs(self):         # PROPOSITION du G0 de collecte l.264
        """`v2/tickers` : symbole à l'indice 0, dernier prix à l'indice 7 (6 dans `v2/ticker` seul), codes UDC et UST
        (pièce l.29, l.50) ; ligne où chaque champ diffère des autres (garde : douze valeurs distinctes)."""
        self.assertEqual(decodeurs.decoder("bitfinex_groupe", lire(FIX, "bitfinex_groupe.bin")), releves(
            "sans_horodatage", ("BTC", "64545", None, {}), ("ETH", "2455.4", None, {}), ("USDC", "1.0001", None, {}),
            ("USDT", "0.99962", None, {})))
        lignes = json.loads(lire(FIX, "bitfinex_groupe.bin"))
        lignes[1] = ["tETHUSD", *range(101, 112)]
        r = decodeurs.decoder("bitfinex_groupe", json.dumps(lignes).encode())
        self.assertEqual((len(set(map(str, lignes[1]))), [x["prix"] for x in r[1] or []]),
                         (12, ["64545", "107", "1.0001", "0.99962"]))

    def test_identifiants_exacts_pannes_identiques_entre_actifs(self):
        """Identifiant manquant, en trop ou répété, ligne de Bitfinex trop courte, prix d'un seul actif nul : la lecture
        entière est `panne_decode` (pannes identiques entre actifs d'un regroupement, déclarées : ADR-0029 l.236)."""
        cg, ll = (json.loads(lire(FIX, n + ".bin")) for n in ("coingecko_groupe", "defillama_groupe"))
        bf = json.loads(lire(FIX, "bitfinex_groupe.bin"))
        cas = [("coingecko_groupe", {k: v for k, v in cg.items() if k != "tether"}),
               ("coingecko_groupe", {**cg, "ripple": cg["tether"]}), ("coingecko_groupe", {**cg, "tether": {
                   **cg["tether"], "usd": 0}}), ("coingecko_groupe", [cg]),
               ("defillama_groupe", {"coins": {k: v for k, v in ll["coins"].items() if k != "coingecko:bitcoin"}}),
               ("defillama_groupe", {"coins": {**ll["coins"], "coingecko:dai": ll["coins"]["coingecko:tether"]}}),
               ("bitfinex_groupe", bf[:3]), ("bitfinex_groupe", bf + [bf[0]]), ("bitfinex_groupe", bf[:3] + [
                   bf[0][:1] + bf[3][1:]]), ("bitfinex_groupe", bf[:3] + [bf[3][:10]]), ("bitfinex_groupe", [
                   *bf[:3], ["tUSTUSD", *bf[3][1:7], "NaN", *bf[3][8:]]])]
        for nom, corps in cas:
            with self.subTest(nom=nom, corps=json.dumps(corps)[:60]):
                self.assertEqual(decodeurs.decoder(nom, json.dumps(corps).encode()), PANNE)

    def test_au_plus_un_releve_par_actif(self):                     # plafond : un relevé par actif (FORMAT §9.1)
        """Plafond du nombre de relevés d'une lecture : un par actif de la liste fermée, quatre au plus ; aucun relevé,
        un actif répété ou hors de la liste : `panne_decode` ; quatre actifs distincts : rendus."""
        quatre = [(a, "1", None, {}) for a in ("BTC", "ETH", "USDC", "USDT")]
        for rendus, statut in (([], "panne_decode"), (quatre[:1] * 2, "panne_decode"), (quatre + quatre[:1],
                               "panne_decode"), ([("XRP", "1", None, {})], "panne_decode"), (quatre, "ok")):
            with self.subTest(rendus=rendus), groupe(*rendus):
                self.assertEqual(decodeurs.decoder("g", b"{}")[0], statut)

    def test_actif_devise_classe_de_la_liste_fermee(self):           # FORMAT §9.1
        for actif, devise, classe, statut in (("XRP", "USD", "agregateur", "panne_decode"),
                                              ("BTC", "EUR", "agregateur", "panne_decode"),
                                              ("BTC", "USD", "oracle_pyth", "panne_decode"),
                                              ("ETH", "USDT", "place_horodatee", "ok")):
            with self.subTest(actif=actif, devise=devise, classe=classe), mock.patch.dict(
                    decodeurs.DECODEURS, h=(actif, devise, classe, lambda j: ("1", None, {}))):
                self.assertEqual(decodeurs.decoder("h", b"{}")[0], statut)


def mots(*m):
    return json.dumps({"jsonrpc": "2.0", "id": 1, "result": "0x" + "".join(f"{x:064x}" for x in m)}).encode()


class Chainlink(unittest.TestCase):             # CB-8b : flux ETH, USDC et USDT (pièce §2 ; Q-CA-08 du G0 de CALIB)
    def test_trois_flux_valeurs_des_fixtures(self):
        """`latestRoundData` sur le proxy principal de chaque flux : réponse au mot 2, 8 décimales, `updatedAt` au mot 4
        (pièce §2 l.63-65 : 2457,46 à 19:26:47Z, 0,99986 à 15:38:23Z, 0,99928672 à 14:38:23Z, date -u -d) ; roundId de
        la phase et du tour (PROPOSITION de CALIB-ACTIFS l.218 : 7 et 34 445, 4 et 26, 4 et 25 ; 2^64 × phase + tour par
        bc) ; plafond de 1,05 (`maxSubmissionValue` 105000000, pièce l.72) porté en extra pour USDC et USDT seuls."""
        plafond = {"plafond": "1.05000000"}
        for nom, actif, prix, ts, extra in (
                ("chainlink_eth", "ETH", "2457.46000000", 1791487607000000, {"round_id": "129127208515966895757"}),
                ("chainlink_usdc", "USDC", "0.99986000", 1791473903000000, {"round_id": "73786976294838206490",
                                                                            **plafond}),
                ("chainlink_usdt", "USDT", "0.99928672", 1791470303000000, {"round_id": "73786976294838206489",
                                                                            **plafond})):
            with self.subTest(nom=nom):
                self.assertEqual(decodeurs.decoder(nom, lire(FIX, nom + ".bin")), ("ok", [
                    {"actif": actif, "classe": "oracle_chainlink", "devise": "USD", "extra": extra, "prix": prix,
                     "ts_source": ts}]))
                self.assertEqual(decodeurs.decoder(nom, mots(7, 1, 2, 3, 7, 7)), PANNE)           # six mots

    def test_plafond_porte_jamais_applique(self):                   # E-C-10, E-C-26 : jugé au recalcul (« borné »)
        """Réponse au-dessus du plafond (2,0) : rendue telle quelle, plafond en extra ; BTC et ETH : aucun plafond. Cinq
        mots distincts (garde : roundId au mot 1, `updatedAt` au mot 4, ni `startedAt` ni `answeredInRound`)."""
        m = (9, 200000000, 1, 1791470303, 8)
        r = {n: decodeurs.decoder(n, mots(*m))[1] or [{}] for n in ("chainlink_btc", "chainlink_eth", "chainlink_usdc",
                                                                   "chainlink_usdt")}
        self.assertEqual((len(set(m)), {n: (x[0].get("prix"), x[0].get("ts_source"), x[0].get("extra")) for n, x in
                                        r.items()}), (5, {
            "chainlink_btc": ("2.00000000", 1791470303000000, {"round_id": "9"}),
            "chainlink_eth": ("2.00000000", 1791470303000000, {"round_id": "9"}),
            "chainlink_usdc": ("2.00000000", 1791470303000000, {"round_id": "9", "plafond": "1.05000000"}),
            "chainlink_usdt": ("2.00000000", 1791470303000000, {"round_id": "9", "plafond": "1.05000000"})}))


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
