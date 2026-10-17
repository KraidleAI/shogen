"""CB-9 (E-C-06 à E-C-08 ; ADR-0029 l.174 ; PROPOSITION l.217 et §2.4 ; G0 de CALIB-ACTIFS, Q-CA-09 et Q-CA-10) :
décodeurs du témoin USDC/USDT, en USDT par USDC. Valeurs hors du code : `docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md`
(l.47, l.87, l.89, l.90, l.94) ; fixtures construites hors du code par bc et printf (outil cité au journal G1) ; prix
d'Uniswap par bc (s²/2^192 exact, arrondi à 50 et à 28 chiffres à la main) ; corps des requêtes écrits à la main
d'après le corps de Chainlink en S2 (`s2-harness/shogen_s2/sources.py` l.278-282) ; doc OKX lue au registre biblio/."""
import json
import os
import unittest
from decimal import ROUND_DOWN, Context, Decimal, DefaultContext, localcontext

from shogen_s2bis.collecte import decodeurs

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "temoin")
PANNE = ("panne_decode", None)
S = 79254659562179534821884273396                                   # sqrtPriceX96 mesuré, bloc 26 149 791 (l.90)
U50 = "1.0006689913764853970918966905584960382210379896029"        # bc : 50 chiffres, le 51e vaut 2
U28 = "1.000668991376485397091896691"                              # bc : 28 chiffres, la suite 558 arrondit en haut
ZERO = "0" * 64


def lire(nom):
    with open(os.path.join(FIX, nom), "rb") as f:
        return f.read()


def rpc(resultat):
    return json.dumps({"jsonrpc": "2.0", "id": 1, "result": resultat}).encode()


def fil_hostile():                                                  # contexte du fil altéré : rien ne doit changer
    return localcontext(Context(prec=3, rounding=ROUND_DOWN, Emin=-9, Emax=9, capitals=0, traps=[]))


def prix(nom, corps):
    statut, valeurs = decodeurs.decoder(nom, corps)
    return (valeurs[0]["prix"], valeurs[0]["ts_source"], valeurs[0]["extra"]) if statut == "ok" else statut


class Okx(unittest.TestCase):
    def test_fixture_de_la_piece(self):
        """l.87 : last 1,00062 ; bid 1,00062 ; ask 1,00063 ; ts 1791487760439 ms (date -u -d @1791487760 :
        2026-10-08 19:29:20 UTC) ; USDC coté en USDT, place horodatée (ts : génération du ticker, doc OKX)."""
        self.assertEqual(decodeurs.decoder("okx_usdc_usdt", lire("okx_usdc_usdt.bin")), ("ok", [
            {"actif": "USDC", "classe": "place_horodatee", "devise": "USDT", "extra": {"askPx": "1.00063",
             "bidPx": "1.00062"}, "prix": "1.00062", "ts_source": 1791487760439000}]))

    def test_instrument_code_et_champs_exiges(self):
        """Autre instrument, code non nul, champ absent, bid ou ask non fini, nul, négatif ou hors des bornes
        d'exposant de CONTEXTE : panne ; ask sous bid admis (« Best ask price may be lower than the best bid price
        during the pre-open period », doc OKX)."""
        j = json.loads(lire("okx_usdc_usdt.bin"))
        d = j["data"][0]
        cas = [{**j, "code": "51001"}] + [{**j, "data": [{**d, "instId": i}]} for i in ("USDT-USD", "usdc-usdt", "")]
        cas += [{**j, "data": [{k: v for k, v in d.items() if k != c}]} for c in ("last", "askPx", "bidPx", "ts")]
        cas += [{**j, "data": [{**d, c: v}]} for c in ("askPx", "bidPx") for v in ("0", "-1", "NaN", "Infinity", "",
                                                                                   "1E+1000000", True, None)]
        for x in cas:
            with self.subTest(x=x["data"][0] if x["data"] else x):
                self.assertEqual(decodeurs.decoder("okx_usdc_usdt", json.dumps(x).encode()), PANNE)
        x = {**j, "data": [{**d, "askPx": "1.0006", "bidPx": "1.0007"}]}
        self.assertEqual(prix("okx_usdc_usdt", json.dumps(x).encode()), ("1.00062", 1791487760439000, {
            "askPx": "1.0006", "bidPx": "1.0007"}))


class Uniswap(unittest.TestCase):
    def test_requete_slot0_construite(self):
        """Corps écrit à la main : pool 0,01 % (l.90), sélecteur de slot0() (l.90), bloc « latest », forme de S2.
        Refus : adresse de 19 octets, sélecteur de 3 octets, argument négatif ou de plus de 32 octets."""
        self.assertEqual(decodeurs.CORPS.get("uniswap_usdc_usdt"), '{"jsonrpc": "2.0", "id": 1, "method": "eth_call", '
                         '"params": [{"to": "0x3416cF6C708Da44DB2624D63ea0AAef7113527C6", "data": "0x3850c7bd"}, '
                         '"latest"]}')
        a = "0x3416cF6C708Da44DB2624D63ea0AAef7113527C6"
        for args in ((a[:-2], "0x3850c7bd"), (a, "0x3850c7"), (a, "0x3850C7BD"), (a, "0x3850c7bd", -1),
                     (a, "0x3850c7bd", 1 << 256), (a, "0x3850c7bd", True)):
            with self.subTest(args=args[1:]):
                self.assertRaises(ValueError, decodeurs.eth_call, *args)
        self.assertEqual(json.loads(decodeurs.eth_call(a, "0x3850c7bd", (1 << 256) - 1, 0))["params"][0]["data"],
                         "0x3850c7bd" + "f" * 64 + ZERO)

    def test_fixture_de_la_piece(self):
        """sqrtPriceX96 de l.90 : prix (s / 2^96)² en 50 chiffres (bc), 1,000669 arrondi (valeur de la pièce) ;
        tick 6 ; décimales 6 et 6 (l.89) ; aucun instant (le bloc n'est pas rendu)."""
        self.assertEqual(decodeurs.decoder("uniswap_usdc_usdt", lire("uniswap_usdc_usdt.bin")), ("ok", [
            {"actif": "USDC", "classe": "sans_horodatage", "devise": "USDT", "extra": {"sqrt_price_x96": str(S),
             "tick": "6"}, "prix": U50, "ts_source": None}]))
        self.assertEqual(round(Decimal(U50), 6), Decimal("1.000669"))

    def test_orientation_borne_et_formes_refusees(self):
        """Prix token1/token0 = s²/2^192 : s = 2^96, 2^97, 2^95 donnent 1, 4 et 0,25 (l'inverse donnerait 0,25 pour
        2^97) ; s = 2^160 − 1 admis, 0 et 2^160 refusés (Q64.96) ; tick signé (−1) ; six ou huit mots, hexadécimal
        non strict, erreur JSON-RPC : panne."""
        reste = lire("uniswap_usdc_usdt.bin").decode()[-7 * 64 + 64 - 2:-2]          # mots 2 à 7 de la fixture
        for s, attendu in ((1 << 96, "1"), (1 << 97, "4"), (1 << 95, "0.25")):
            self.assertEqual(prix("uniswap_usdc_usdt", rpc("0x" + f"{s:064x}" + reste))[0], attendu)
        grand = prix("uniswap_usdc_usdt", rpc("0x" + f"{(1 << 160) - 1:064x}" + reste))
        self.assertEqual(grand[0], "340282366920938463463374607431768211455.99999999953")     # bc, 50 chiffres
        moins_un = "0x" + f"{S:064x}" + "f" * 64 + reste[64:]
        self.assertEqual(prix("uniswap_usdc_usdt", rpc(moins_un))[2], {"sqrt_price_x96": str(S), "tick": "-1"})
        for r in ("0x" + ZERO + reste, "0x" + f"{1 << 160:064x}" + reste, "0x" + f"{S:064x}" + reste[64:],
                  "0x" + f"{S:064x}" + reste + ZERO, "0x" + f"{S:064x}" + reste[:-1] + "g", " 0x" + f"{S:064x}" + reste,
                  None, 7):
            with self.subTest(r=str(r)[:12]):
                self.assertEqual(decodeurs.decoder("uniswap_usdc_usdt", rpc(r)), PANNE)
        erreur = b'{"jsonrpc":"2.0","id":1,"error":{"code":-32000,"message":"execution reverted"}}'
        self.assertEqual(decodeurs.decoder("uniswap_usdc_usdt", erreur), PANNE)

    def test_contexte_nomme_jamais_celui_du_fil(self):                # E-C-07 ; PROPOSITION §2.4, « Décodeurs »
        """Sous un contexte du fil altéré (3 chiffres, troncature), le prix reste celui des 50 chiffres, par
        `decoder` comme par le décodeur appelé seul ; garde d'attendu : le contexte par défaut (28 chiffres) rend une
        autre chaîne, celle de bc, et la fixture sépare donc les deux contextes."""
        with fil_hostile():
            r = decodeurs.decoder("uniswap_usdc_usdt", lire("uniswap_usdc_usdt.bin"))
            seul = decodeurs._uniswap(json.loads(lire("uniswap_usdc_usdt.bin")))[0]
        self.assertEqual((r[1] and r[1][0]["prix"], str(seul)), (U50, U50))
        with localcontext(DefaultContext):
            self.assertEqual(str(Decimal(S * S) / (1 << 192)), U28)


if __name__ == "__main__":
    unittest.main()
