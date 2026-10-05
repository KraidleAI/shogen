"""CB-3, E-C-03, E-C-17 : lecture typée, requête, analyse de la réponse sur flux injecté. Requêtes recopiées des octets
d'urllib (forme de S2, serveur de boucle locale) ; base64 et sha256 du corps par printf, base64 et sha256sum."""
import time
import unittest

from shogen_s2bis.collecte import http
from shogen_s2bis.collecte.lecture import S, Lecture, horloge

UA = "User-Agent: Mozilla/5.0 (Shogen-S2-harness; +https://github.com/KraidleAI/shogen)\r\n"
REQUETE = ("GET /v1/btc?x=1 HTTP/1.1\r\nAccept-Encoding: identity\r\nHost: api.example\r\n" + UA +
           "Accept: application/json\r\nConnection: close\r\n\r\n").encode()
POST = ("POST / HTTP/1.1\r\nAccept-Encoding: identity\r\nContent-Length: 8\r\nHost: rpc.example:8545\r\n" + UA +
        'Accept: application/json\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n{"a": 1}').encode()
CORPS, B64 = b'{"p":1}', "eyJwIjoxfQ=="
SHA, VIDE = ("4835f96cb95414c1b3dd5816bcabc7ae1405283accdbdf990de0f35f07075abb",
             "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
OK7 = b"HTTP/1.1 200 OK\r\nContent-Length: 7\r\n\r\n" + CORPS                         # 45 octets (wc -c)
MORCEAUX = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n3\r\n{\"p\r\n"


def flux(*morceaux):
    """`recevoir` injecté : un morceau par appel (coupé au tampon), puis la fin (0) ; une exception est levée."""
    reste = list(morceaux)

    def recevoir(tampon):
        m = reste.pop(0) if reste else b""
        if isinstance(m, BaseException):
            raise m
        n = min(len(m), len(tampon))
        tampon[:n] = m[:n]
        reste[:0] = [m[n:]] if n < len(m) else []
        return n
    return recevoir


class Requete(unittest.TestCase):
    def test_octets_get_et_post_egaux_a_ceux_d_urllib(self):
        self.assertEqual(http.octets(http.Requete("api.example", "/v1/btc?x=1")), REQUETE)
        self.assertEqual(http.octets(http.Requete("rpc.example", "/", 8545, "POST", b'{"a": 1}')), POST)

    def test_hors_ascii_imprimable_refuse(self):
        for hote, chemin, methode in (("api.example", "/x\r\nX-Injecte: 1", "GET"), ("api example", "/", "GET"),
                                      ("", "/", "GET"), ("api.example", "/é", "GET"), ("api.example", "/", "GE T")):
            with self.subTest(hote=hote, chemin=chemin, methode=methode), self.assertRaises(http.Panne) as c:
                http.octets(http.Requete(hote, chemin, methode=methode))
            self.assertEqual(c.exception.sous_type, "autre")


class Analyse(unittest.TestCase):
    def panne(self, *morceaux, plafond=http.PLAFOND):
        with self.assertRaises(http.Panne) as c:
            http.analyser(flux(*morceaux), plafond)
        return c.exception.sous_type

    def test_corps_annonce_par_morceaux_ou_jusqu_a_la_fermeture(self):
        for morceaux, attendu in (((OK7,), (200, CORPS)), ((OK7[:20], OK7[20:39], OK7[39:]), (200, CORPS)),
                                  ((MORCEAUX + b"4\r\n\":1}\r\n0\r\n\r\n",), (200, CORPS)),
                                  ((b"HTTP/1.1 451 Refus\r\nContent-Length: 2\r\n\r\nno",), (451, b"no")),
                                  ((b"HTTP/1.0 200 OK\r\n\r\n", CORPS), (200, CORPS))):
            with self.subTest(morceaux=morceaux):
                self.assertEqual(http.analyser(flux(*morceaux)), attendu)

    def test_coupure(self):
        """Corps plus court qu'annoncé (régression de l'essai 1 de la PROPOSITION, §9), flux vide, en-têtes coupés."""
        for morceaux in ((b"HTTP/1.1 200 OK\r\nContent-Length: 100\r\n\r\n0123456789",), (MORCEAUX,), (),
                         (b"HTTP/1.1 200 OK\r\nContent-Le",), (b"HTTP/1.1 200 O",)):
            with self.subTest(morceaux=morceaux):
                self.assertEqual(self.panne(*morceaux), "coupure")

    def test_reponse_illisible(self):
        for morceaux in ((b"charabia\r\n\r\n",), (b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\nzz\r\n",),
                         (b"HTTP/1.1 99 Trop bas\r\n\r\n",)):
            with self.subTest(morceaux=morceaux):
                self.assertEqual(self.panne(*morceaux), "autre")

    def test_plafond_et_panne_du_flux_transmise(self):
        self.assertEqual(http.analyser(flux(OK7), len(OK7)), (200, CORPS))
        self.assertEqual(self.panne(OK7, plafond=len(OK7) - 1), "autre")
        self.assertEqual(self.panne(OK7[:20], http.Panne("delai")), "delai")


class LectureTypee(unittest.TestCase):
    def test_enregistrement(self):
        self.assertEqual(Lecture("ok", 10, 20, {"dns": 11}, "127.0.0.1:443", code=200, octets=CORPS).enregistrement(),
                         {"statut": "ok", "sous_type": None, "code": 200, "depart": 10, "fin": 20, "adresse":
                          "127.0.0.1:443", "phases": {"dns": 11}, "valeurs": None, "brut": B64, "sha256": SHA})
        self.assertEqual(Lecture("panne_transport", 0, 0, sous_type="coupure").enregistrement()["sha256"], VIDE)

    def test_statut_et_sous_type_controles(self):
        for statut, sous_type in (("ok", "dns"), ("panne_transport", None), ("panne_transport", "x"), ("panne", None),
                                  ("panne_http", "delai")):
            with self.subTest(statut=statut, sous_type=sous_type):
                self.assertRaises(ValueError, Lecture, statut, 0, 0, sous_type=sous_type)

    def test_horloge_entiere_en_microsecondes(self):
        a = horloge()
        self.assertTrue(type(a) is int and abs(a - time.time() * S) < S, a)
