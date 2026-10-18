"""CB-9 (E-C-06 à E-C-08 ; ADR-0029 l.174 ; PROPOSITION l.217 et §2.4 ; G0 de CALIB-ACTIFS, Q-CA-09 et Q-CA-10) :
décodeurs du témoin USDC/USDT, en USDT par USDC. Valeurs hors du code : `docs/adr-0029/g0-calib/PAIRES-ET-TEMOIN.md`
(l.47, l.87, l.89, l.90, l.94) ; fixtures construites hors du code par bc et printf (outil cité au journal G1) ; prix
d'Uniswap par bc (s²/2^192 exact, arrondi à 50 et à 28 chiffres à la main) ; corps des requêtes écrits à la main
d'après le corps de Chainlink en S2 (`s2-harness/shogen_s2/sources.py` l.278-282) ; doc OKX lue au registre biblio/.
GEL-5 (SHOGEN-S2BIS-TEMOIN-BLOC-1 ; avis de l'advisor du lot, Q-B, option 2 encadrée) : requête groupée
[eth_blockNumber (id 1), eth_call (id 2), eth_blockNumber (id 3)] écrite à la main ; fixtures réécrites à la main en
réponses groupées : Uniswap dans l'ordre, blocs 26 149 791 (0x18f039f, printf) aux deux bouts (bloc de la pièce,
l.90) ; Curve dans l'ordre 3, 1, 2, blocs 26 149 796 (0x18f03a4, bloc de la pièce, l.94) et 26 149 797 (0x18f03a5,
un bloc de plus, valeur de test)."""
import json
import os
import tempfile
import unittest
from decimal import ROUND_DOWN, Context, Decimal, DefaultContext, localcontext
from unittest import mock

from shogen_s2bis.collecte import decodeurs, entree, http
from shogen_s2bis.collecte.lecture import Lecture
from tests.test_entree import COMMIT, configurations, refus
from tests.test_secondaire import carte, fichiers

LOT_U = ('[{"jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber", "params": []}, '
         '{"jsonrpc": "2.0", "id": 2, "method": "eth_call", "params": [{"to": '
         '"0x3416cF6C708Da44DB2624D63ea0AAef7113527C6", "data": "0x3850c7bd"}, "latest"]}, '
         '{"jsonrpc": "2.0", "id": 3, "method": "eth_blockNumber", "params": []}]')    # GEL-5, écrite à la main
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "temoin")
PANNE = ("panne_decode", None)
S = 79254659562179534821884273396                                   # sqrtPriceX96 mesuré, bloc 26 149 791 (l.90)
U50 = "1.0006689913764853970918966905584960382210379896029"        # bc : 50 chiffres, le 51e vaut 2
U28 = "1.000668991376485397091896691"                              # bc : 28 chiffres, la suite 558 arrondit en haut
ZERO = "0" * 64
LIMITES = ("identité de la source `master` avec le bytecode déployé non vérifiée",              # C-P2D-2
           "rattachement direct du pool NG à sa fabrique non lu",
           "absence du bogue d'oracle du pool NG non vérifiée sur chaîne")


def lire(nom):
    with open(os.path.join(FIX, nom), "rb") as f:
        return f.read()


B, BLOCS = "0x18f039f", {"bloc_avant": "26149791", "bloc_apres": "26149791"}      # printf '%x' 26149791 (l.90)


def rpc(resultat, avant=B, apres=B, **remplace):
    """Réponse groupée (GEL-5) : blocs en id 1 et 3, `resultat` en id 2 ; `remplace` : {id : élément} substitué."""
    lot = [{"jsonrpc": "2.0", "id": 1, "result": avant}, {"jsonrpc": "2.0", "id": 2, "result": resultat},
           {"jsonrpc": "2.0", "id": 3, "result": apres}]
    return json.dumps([remplace.get(f"r{x['id']}", x) for x in lot]).encode()


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
            {"actif": "USDC", "classe": "temoin", "devise": "USDT", "extra": {"askPx": "1.00063",
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
        self.assertEqual(decodeurs.CORPS.get("uniswap_usdc_usdt"), LOT_U)              # GEL-5 : requête groupée
        a = "0x3416cF6C708Da44DB2624D63ea0AAef7113527C6"
        for args in ((a[:-2], "0x3850c7bd"), (a, "0x3850c7"), (a, "0x3850C7BD"), (a, "0x3850c7bd", -1),
                     (a, "0x3850c7bd", 1 << 256), (a, "0x3850c7bd", True)):
            with self.subTest(args=args[1:]):
                self.assertRaises(ValueError, decodeurs.eth_call, *args)
        self.assertEqual(json.loads(decodeurs.eth_call(a, "0x3850c7bd", (1 << 256) - 1, 0))["params"][0]["data"],
                         "0x3850c7bd" + "f" * 64 + ZERO)

    def test_fixture_de_la_piece(self):
        """sqrtPriceX96 de l.90 : prix (s / 2^96)² en 50 chiffres (bc), 1,000669 arrondi (valeur de la pièce) ;
        tick 6 ; décimales 6 et 6 (l.89) ; aucun instant ; blocs encadrants en extra (GEL-5)."""
        self.assertEqual(decodeurs.decoder("uniswap_usdc_usdt", lire("uniswap_usdc_usdt.bin")), ("ok", [
            {"actif": "USDC", "classe": "temoin", "devise": "USDT", "extra": {"sqrt_price_x96": str(S),
             "tick": "6", **BLOCS}, "prix": U50, "ts_source": None}]))
        self.assertEqual(round(Decimal(U50), 6), Decimal("1.000669"))

    def test_orientation_borne_et_formes_refusees(self):
        """Prix token1/token0 = s²/2^192 : s = 2^96, 2^97, 2^95 donnent 1, 4 et 0,25 (l'inverse donnerait 0,25 pour
        2^97) ; s = 2^160 − 1 admis, 0 et 2^160 refusés (Q64.96) ; tick signé (−1) ; six ou huit mots, hexadécimal
        non strict, erreur JSON-RPC : panne."""
        reste = json.loads(lire("uniswap_usdc_usdt.bin"))[1]["result"][2 + 64:]      # mots 2 à 7 de la fixture
        for s, attendu in ((1 << 96, "1"), (1 << 97, "4"), (1 << 95, "0.25")):
            self.assertEqual(prix("uniswap_usdc_usdt", rpc("0x" + f"{s:064x}" + reste))[0], attendu)
        grand = prix("uniswap_usdc_usdt", rpc("0x" + f"{(1 << 160) - 1:064x}" + reste))
        self.assertEqual(grand[0], "340282366920938463463374607431768211455.99999999953")     # bc, 50 chiffres
        moins_un = "0x" + f"{S:064x}" + "f" * 64 + reste[64:]
        self.assertEqual(prix("uniswap_usdc_usdt", rpc(moins_un))[2], {"sqrt_price_x96": str(S), "tick": "-1",
                                                                        **BLOCS})
        for r in ("0x" + ZERO + reste, "0x" + f"{1 << 160:064x}" + reste, "0x" + f"{S:064x}" + reste[64:],
                  "0x" + f"{S:064x}" + reste + ZERO, "0x" + f"{S:064x}" + reste[:-1] + "g", " 0x" + f"{S:064x}" + reste,
                  None, 7):
            with self.subTest(r=str(r)[:12]):
                self.assertEqual(decodeurs.decoder("uniswap_usdc_usdt", rpc(r)), PANNE)
        erreur = {"jsonrpc": "2.0", "id": 2, "error": {"code": -32000, "message": "execution reverted"}}
        self.assertEqual(decodeurs.decoder("uniswap_usdc_usdt", rpc(None, r2=erreur)), PANNE)

    def test_contexte_nomme_jamais_celui_du_fil(self):                # E-C-07 ; PROPOSITION §2.4, « Décodeurs »
        """Sous un contexte du fil altéré (3 chiffres, troncature), le prix reste celui des 50 chiffres, par
        `decoder` comme par le décodeur appelé seul ; garde d'attendu : le contexte par défaut (28 chiffres) rend une
        autre chaîne, celle de bc, et la fixture sépare donc les deux contextes."""
        with fil_hostile():
            r = decodeurs.decoder("uniswap_usdc_usdt", lire("uniswap_usdc_usdt.bin"))
            seul = decodeurs._uniswap(json.loads(lire("uniswap_usdc_usdt.bin"))[1])[0]
        self.assertEqual((r[1] and r[1][0]["prix"], str(seul)), (U50, U50))
        with localcontext(DefaultContext):
            self.assertEqual(str(Decimal(S * S) / (1 << 192)), U28)


class Curve(unittest.TestCase):                                   # CB-9b ; Q-CA-09 : 3pool, get_dy(1, 2, 10^6)
    MAX = "1.1579208923731619542357098500868790785326998466564E+71"   # bc : (2^256 − 1) / 10^6, 50 chiffres

    def test_requete_get_dy_construite(self):
        """Corps écrit à la main : 3pool (l.94), sélecteur de get_dy (l.94), i = 1 (USDC), j = 2 (USDT), dx = 10^6
        (1 USDC à 6 décimales ; 10^6 = 0xf4240 par printf), chacun sur 32 octets."""
        data = "0x5e0d443f" + "0" * 63 + "1" + "0" * 63 + "2" + "0" * 59 + "f4240"
        self.assertEqual(decodeurs.CORPS.get("curve_usdc_usdt"), LOT_U.replace(
            "0x3416cF6C708Da44DB2624D63ea0AAef7113527C6", "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7").replace(
            "0x3850c7bd", data))

    def test_fixture_de_la_piece(self):
        """l.94 : get_dy(1, 2, 10^6) = 1 000 393, soit 1,000393 USDT pour 1 USDC, net des frais ; aucun instant ;
        réponses dans l'ordre 3, 1, 2, appariées par `id` ; blocs 26 149 796 et 26 149 797 (GEL-5)."""
        self.assertEqual(decodeurs.decoder("curve_usdc_usdt", lire("curve_usdc_usdt.bin")), ("ok", [
            {"actif": "USDC", "classe": "temoin", "devise": "USDT", "extra": {
                "dy": "1000393", "bloc_avant": "26149796", "bloc_apres": "26149797"}, "prix": "1.000393",
             "ts_source": None}]))

    def test_decimales_portees_par_les_deux_pieces(self):
        """Décimales distinctes (USDT à 18, valeur de test) : le prix de chaque pièce est multiplié par 10^(6 − 18),
        valeurs écrites à la main ; D_USDC et D_USDT permutées donneraient 10^12."""
        with mock.patch.object(decodeurs, "D_USDT", 18):
            self.assertEqual([prix(n, lire(n + ".bin"))[0] for n in ("uniswap_usdc_usdt", "curve_usdc_usdt")],
                             [U50 + "E-12", "1.000393E-12"])

    def test_limites_de_la_lecture_declarees(self):                 # C-P2D-2 ; SHOGEN-S2BIS-CURVE-DOC-1
        """Docstring du décodeur : sens lu (unités natives, net des frais, source `StableSwap3Pool.vy`), les trois
        limites de la lecture du 2026-10-17 (adjudication de la tranche D, ajout daté), `price_oracle` non retenu."""
        doc = " ".join(decodeurs._curve.__doc__.split())
        self.assertEqual([x in doc for x in LIMITES + ("StableSwap3Pool.vy", "unités natives", "C-P2D-2",
                                                       "`price_oracle`")], [True] * 7)

    def test_mot_maximal_et_formes_refusees(self):
        """dy = 2^256 − 1 : 50 chiffres (bc), sous un contexte du fil altéré, par `decoder` comme par le décodeur
        appelé seul ; garde : le contexte par défaut rend 28 chiffres. dy nul, deux mots, 63 chiffres, erreur
        JSON-RPC : panne."""
        with fil_hostile():
            r = prix("curve_usdc_usdt", rpc("0x" + "f" * 64))
            seul = decodeurs._curve({"result": "0x" + "f" * 64})[0]
        self.assertEqual((r[0], str(seul), r[2]), (self.MAX, self.MAX, {"dy": str((1 << 256) - 1), **BLOCS}))
        with localcontext(DefaultContext):
            self.assertEqual(str(Decimal((1 << 256) - 1) / 10 ** 6), "1.157920892373161954235709850E+71")
        for x in (rpc("0x" + ZERO), rpc("0x" + ZERO + f"{1000393:064x}"), rpc("0x" + ZERO[1:]), rpc(1000393),
                  rpc(None, r2={"jsonrpc": "2.0", "id": 2, "error": {"code": -32000, "message": "reverted"}})):
            with self.subTest(x=x[:48]):
                self.assertEqual(decodeurs.decoder("curve_usdc_usdt", x), PANNE)


class Lot(unittest.TestCase):                                     # GEL-5 ; SHOGEN-S2BIS-TEMOIN-BLOC-1
    MOT = "0x" + f"{1000393:064x}"

    def test_blocs_encadrants_apparies_par_id(self):
        """Ordre quelconque, apparié par `id` ; blocs égaux ou à un bloc d'écart, en décimal ; tout le reste en panne
        entière : lot incomplet ou de quatre, `id` répété, en texte ou décimal, élément `error` (même avec un
        `result`), réponse sans `result`, bloc hors de l'hexadécimal strict ou de 64 bits, ou `bloc_apres` <
        `bloc_avant` ; une réponse seule (forme d'avant GEL-5) aussi."""
        lot = json.loads(rpc(self.MOT, "0xa", "0xb"))
        for ordre in ((0, 1, 2), (2, 1, 0), (1, 2, 0)):
            self.assertEqual(prix("curve_usdc_usdt", json.dumps([lot[i] for i in ordre]).encode())[2],
                             {"dy": "1000393", "bloc_avant": "10", "bloc_apres": "11"})
        un = {"jsonrpc": "2.0", "id": 1, "result": B}
        cas = [json.dumps(lot[:2]), json.dumps(lot + [lot[0]]), json.dumps([lot[0], lot[1], un]),
               rpc(self.MOT, r1={**un, "id": "1"}), rpc(self.MOT, r1={**un, "id": 1.0}),
               rpc(self.MOT, r3={"jsonrpc": "2.0", "id": 3, "error": {"code": -32000}}),
               rpc(self.MOT, r1={**un, "error": None}), rpc(self.MOT, r3={"jsonrpc": "2.0", "id": 3}),
               rpc(self.MOT, apres="0xb", avant="0xc"), json.dumps(lot[1]), rpc(self.MOT, apres="0x1g")]
        cas += [rpc(self.MOT, avant=b, apres=b) for b in ("0x", "0x1g", "26149791", "0X18f039f", " 0x1",
                                                          "0x" + "f" * 17, 7, None)]   # deux bouts égaux : le bloc seul
        for x in cas:
            with self.subTest(x=str(x)[:60]):
                self.assertEqual(decodeurs.decoder("curve_usdc_usdt", x if type(x) is bytes else x.encode()), PANNE)
        self.assertEqual(prix("uniswap_usdc_usdt", rpc("0x" + f"{S:064x}" + "0" * 384, "0x" + "f" * 16, "0x" + "f" *
                                                       16))[2]["bloc_apres"], str((1 << 64) - 1))


class Classe(unittest.TestCase):                                  # C-P2D-1 (adjudication Q-1 de la tranche D)
    def test_classe_temoin_pour_les_trois_lectures(self):
        """Les trois lectures du témoin, et elles seules, sont de classe `temoin` (ADR-0029 l.174 : « hors des
        classes USD et hors du vote ») ; liste fermée des classes : les quatre du recalcul, puis `temoin`."""
        self.assertEqual(sorted(n for n, x in decodeurs.DECODEURS.items() if x[2] == "temoin"),
                         ["curve_usdc_usdt", "okx_usdc_usdt", "uniswap_usdc_usdt"])
        self.assertEqual(decodeurs.CLASSES, ("place_horodatee", "sans_horodatage", "agregateur", "oracle_chainlink",
                                             "temoin"))


class Configuration(unittest.TestCase):                           # CB-9c ; SHOGEN-S2BIS-TEMOIN-RPC-1 (annexe B, B.81)
    """Hôtes RPC du témoin retenus (Q-CA-10 du G0 de CALIB-ACTIFS) : `eth.drpc.org` pour Uniswap, `rpc.mevblocker.io`
    pour Curve ; Chainlink : `ethereum-rpc.publicnode.com` (ADR-0029 l.168). Écrits ici, en configuration de test."""
    HOTES = {"chainlink_btc": "ethereum-rpc.publicnode.com", "uniswap_usdc_usdt": "eth.drpc.org",
             "curve_usdc_usdt": "rpc.mevblocker.io", "okx_usdc_usdt": "www.okx.com"}

    def formes(self, **hotes):
        """formes.json de test : une forme par décodeur, nommée autrement que lui (hôte de HOTES, ou de `hotes`),
        corps du décodeur lu sur chaîne ; les autres configurations de test_entree."""
        f, s, d = configurations(443)
        modele = {**f["formes"][0], "chemin": "/", "methode": "POST"}
        f["formes"] = [{**modele, "nom": "f-" + n, "decodeur": n, "hote": hotes.get(n, h),
                        "corps": decodeurs.CORPS.get(n, "{}")} for n, h in self.HOTES.items()]
        f["formes"][3].update(methode="GET", corps="", chemin="/api/v5/market/ticker?instId=USDC-USDT")
        return f, s, d

    def charger(self, f, s, d):
        with tempfile.TemporaryDirectory() as t:
            chemins = {}
            for nom, x in (("formes", f), ("sante", s), ("descripteur", d)):
                chemins[nom] = os.path.join(t, nom + ".json")
                with open(chemins[nom], "w", encoding="utf-8") as fichier:
                    json.dump(x, fichier)
            return refus(lambda: entree.configurer(chemins, COMMIT))

    def test_corps_lie_au_decodeur(self):
        """Uniswap et Curve : `POST` du corps exact de leur décodeur ; corps de l'autre pièce, bloc autre que
        « latest », `GET` sans corps : refus `corps-du-decodeur`."""
        f, s, d = self.formes()
        self.assertIsNone(self.charger(f, s, d))
        autre = dict(enumerate(({"corps": decodeurs.CORPS.get("curve_usdc_usdt")},
                                {"corps": str(decodeurs.CORPS.get("uniswap_usdc_usdt")).replace("latest", "pending")},
                                {"methode": "GET", "corps": ""})))
        for k, x in autre.items():
            g = json.loads(json.dumps(f))
            g["formes"][1].update(x)
            with self.subTest(cas=k):
                self.assertEqual(str(self.charger(g, s, d))[:37], "CONFIG/incoherent : corps-du-decodeur")

    def test_une_unite_sur_chaine_un_hote_rpc(self):
        """Une unité sur chaîne = un hôte RPC (ADR-0029 l.174) : Uniswap sur l'hôte de Chainlink, Curve sur celui
        d'Uniswap : refus `rpc-par-unite` ; deux flux de la classe de Chainlink (un flux injecté de plus) sur un
        seul hôte : admis, sur deux : refusé ; OKX (hors chaîne) sur l'hôte d'Uniswap : admis."""
        cas = [({}, None), ({"uniswap_usdc_usdt": "ethereum-rpc.publicnode.com"}, "rpc-par-unite"),
               ({"curve_usdc_usdt": "eth.drpc.org"}, "rpc-par-unite"), ({"okx_usdc_usdt": "eth.drpc.org"}, None)]
        for hotes, regle in cas:
            with self.subTest(hotes=hotes):
                r = self.charger(*self.formes(**hotes))
                self.assertEqual(r and r.split(" : ")[:2], regle and ["CONFIG/incoherent", regle])
        f, s, d = self.formes()
        eth = {**f["formes"][0], "nom": "eth", "decodeur": "chainlink_eth"}
        with mock.patch.dict(decodeurs.DECODEURS, chainlink_eth=("ETH", "USD", "oracle_chainlink", lambda j: j)):
            for hote, regle in (("ethereum-rpc.publicnode.com", None), ("ethereum.publicnode.com", "rpc-par-unite")):
                with self.subTest(hote=hote):
                    r = self.charger({**f, "places": 5, "formes": f["formes"] + [{**eth, "hote": hote}]}, s, d)
                    self.assertEqual(r and r.split(" : ")[:2], regle and ["CONFIG/incoherent", regle])
        self.assertEqual([decodeurs.unite_sur_chaine(n) for n in ("chainlink_btc", "uniswap_usdc_usdt",
                                                                    "curve_usdc_usdt", "okx_usdc_usdt", "inconnu")],
                         ["chainlink", "uniswap", "curve", None, None])

    def test_regles_aussi_dans_la_carte(self):
        """`carte.json` porte les mêmes règles de forme (COHERENCE_CARTE) : corps d'Uniswap altéré, Uniswap et Curve
        sur un hôte : refus nommés ; les deux pièces chacune sur son hôte : admis."""
        f, _s, d = configurations(1)
        x = {**carte(1)["formes"][0], "methode": "POST", "chemin": "/"}
        u = {**x, "nom": "u", "decodeur": "uniswap_usdc_usdt", "corps": decodeurs.CORPS.get("uniswap_usdc_usdt", "{}")}
        c = {**x, "nom": "c", "decodeur": "curve_usdc_usdt", "corps": decodeurs.CORPS.get("curve_usdc_usdt", "{}")}
        cas = [([u, {**c, "hote": "127.0.0.2"}], None), ([{**u, "corps": "{}"}], "corps-du-decodeur"),
               ([u, c], "rpc-par-unite")]
        with tempfile.TemporaryDirectory() as t:
            for formes, regle in cas:
                with self.subTest(regle=regle):
                    r = refus(lambda: entree.configurer_secondaire(fichiers(t, formes=f, carte=carte(1, formes=formes),
                                                                            descripteur=d), COMMIT))
                    self.assertEqual(r and r.split(" : ")[:2], regle and ["CONFIG/incoherent", regle])

    def test_requetes_construites_hote_de_la_configuration(self):
        """Câblage (`construire`) : chaque requête porte l'hôte de sa forme et le corps de son décodeur ; octets de
        la requête d'Uniswap écrits à la main (FORMAT §9.3) ; réponses servies par les fixtures, décodées. Aucun envoi :
        `http.lire` est remplacé."""
        f, s, d = self.formes()
        vues, servies = {}, {"uniswap_usdc_usdt": "uniswap_usdc_usdt.bin", "curve_usdc_usdt": "curve_usdc_usdt.bin",
                             "okx_usdc_usdt": "okx_usdc_usdt.bin", "chainlink_btc": "uniswap_usdc_usdt.bin"}

        def lire_faux(req, suivi, delai, tls):
            vues[req.hote] = req
            nom = next(n for n, h in self.HOTES.items() if h == req.hote)
            return Lecture("ok", 1, 2, code=200, octets=lire(servies[nom]))
        with tempfile.TemporaryDirectory() as t, mock.patch.object(entree.http, "lire", side_effect=lire_faux):
            lus = {n: entree.construire(f, s, d, t)[1].lectures["f-" + n]({}) for n in self.HOTES}
        corps = LOT_U
        self.assertEqual(http.octets(vues["eth.drpc.org"]), (
            "POST / HTTP/1.1\r\nAccept-Encoding: identity\r\nContent-Length: %d\r\nHost: eth.drpc.org\r\n"
            "User-Agent: Mozilla/5.0 (Shogen-S2-harness; +https://github.com/KraidleAI/shogen)\r\n"
            "Accept: application/json\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n%s"
            % (len(corps), corps)).encode())
        self.assertEqual({h: (r.methode, r.chemin, r.corps and r.corps.decode()) for h, r in vues.items()}, {
            "ethereum-rpc.publicnode.com": ("POST", "/", "{}"), "eth.drpc.org": ("POST", "/", corps),
            "rpc.mevblocker.io": ("POST", "/", decodeurs.CORPS.get("curve_usdc_usdt")),
            "www.okx.com": ("GET", "/api/v5/market/ticker?instId=USDC-USDT", None)})
        self.assertEqual({n: (x.statut, x.valeurs and x.valeurs[0]["prix"]) for n, x in lus.items()}, {
            "chainlink_btc": ("panne_decode", None), "uniswap_usdc_usdt": ("ok", U50),
            "curve_usdc_usdt": ("ok", "1.000393"), "okx_usdc_usdt": ("ok", "1.00062")})

    def test_aucun_hote_en_dur_dans_les_decodeurs(self):
        """Le code des décodeurs ne nomme aucun hôte (ni ceux de PAIRES-ET-TEMOIN §3.2, ni celui d'OKX) : l'hôte
        est celui de la forme (SHOGEN-S2BIS-TEMOIN-RPC-1)."""
        with open(decodeurs.__file__, encoding="utf-8") as fichier:
            source = fichier.read().lower()
        hotes = ["publicnode", "drpc", "mevblocker", "blastapi", "tenderly", "1rpc", "ankr", "cloudflare-eth",
                 "llamarpc", "merkle.io", "flashbots", "meowrpc", "omniatech", "blockpi", "payload.de", "okx.com",
                 "https:", "http:"]
        self.assertEqual([h for h in hotes if h in source], [])


if __name__ == "__main__":
    unittest.main()
