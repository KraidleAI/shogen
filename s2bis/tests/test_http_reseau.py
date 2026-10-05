"""CB-3, E-C-03 à E-C-05 : lecture par phases sur serveurs factices de boucle locale, résolveur injecté."""
import socket
import ssl
import struct
import threading
import time
import unittest

from shogen_s2bis.collecte import http
from shogen_s2bis.collecte.lecture import S, horloge
from tests.test_http import CORPS, OK7, REQUETE


def servir(comportement):
    """Serveur d'une connexion sur 127.0.0.1, servie par `comportement(conn, recues)` ; rend (port, recues, fil)."""
    srv, recues = socket.create_server(("127.0.0.1", 0)), []

    def fil():
        with srv:
            srv.settimeout(10)
            try:
                with srv.accept()[0] as conn:
                    conn.settimeout(10)
                    comportement(conn, recues)
            except OSError:                                         # aucun client, ou client parti : fin du service
                pass
    t = threading.Thread(target=fil, daemon=True)
    t.start()
    return srv.getsockname()[1], recues, t


def repondre(octets, rst=False, pas=0):
    """Lit la requête (jusqu'à la ligne vide), envoie `octets` (un octet toutes les `pas` s si `pas`), RST si `rst`."""
    def comportement(conn, recues):
        recu = b""
        while b"\r\n\r\n" not in recu and (bloc := conn.recv(4096)):
            recu += bloc
        recues.append(recu)
        for morceau in [octets[i:i + 1] for i in range(len(octets))] if pas else [octets]:
            time.sleep(pas)
            conn.sendall(morceau)
        if rst:                                                     # SO_LINGER nul : la fermeture envoie un RST
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    return comportement


class Resolveur:
    """getaddrinfo injecté : note ses arguments, attend, lève `erreur`, ou rend 127.0.0.1:`port` puis 127.0.0.2:1."""
    def __init__(self, port, erreur=None, pause=0):
        self.port, self.erreur, self.pause, self.appels = port, erreur, pause, []

    def __call__(self, *args):
        self.appels.append(args)
        time.sleep(self.pause)
        if self.erreur:
            raise self.erreur
        a = (socket.AF_INET, socket.SOCK_STREAM, 6, "")
        return [] if self.port is None else [(*a, ("127.0.0.1", self.port)), (*a, ("127.0.0.2", 1))]


class Client(unittest.TestCase):
    def lire(self, comportement, req=http.Requete("api.example", "/v1/btc?x=1"), **k):
        port, recues, fil = servir(comportement)
        self.res = Resolveur(port)
        lu = http.lire(req, resoudre=self.res, **{"delai": 2 * S, "tls": None, **k})
        fil.join(10)
        return lu, recues, port

    def test_reponse_200_phases_ipv4(self):
        lu, recues, port = self.lire(repondre(OK7))
        self.assertEqual((lu.statut, lu.sous_type, lu.code, lu.octets, lu.adresse, recues),
                         ("ok", None, 200, CORPS, f"127.0.0.1:{port}", [REQUETE]))
        self.assertEqual(self.res.appels, [("api.example", 443, socket.AF_INET, socket.SOCK_STREAM)])
        instants = [lu.depart, *(lu.phases[p] for p in ("dns", "connexion", "requete", "corps")), lu.fin]
        self.assertEqual((sorted(lu.phases), sorted(instants)), (["connexion", "corps", "dns", "requete"], instants))

    def test_codes_http(self):
        for code in (301, 403, 429, 451):
            with self.subTest(code=code):
                lu = self.lire(repondre(b"HTTP/1.1 %d Refus\r\nContent-Length: 2\r\n\r\nno" % code))[0]
                self.assertEqual((lu.statut, lu.sous_type, lu.code, lu.octets), ("panne_http", None, code, b"no"))

    def test_corps_coupe_ou_reponse_vide(self):                      # essai 1 de la PROPOSITION (§9), en réel
        tete = b"HTTP/1.1 200 OK\r\nContent-Length: 100\r\n\r\n0123456789"
        for comportement in (repondre(tete, rst=True), repondre(tete), repondre(b"")):
            with self.subTest(comportement=comportement):
                lu = self.lire(comportement)[0]
                self.assertEqual((lu.statut, lu.sous_type, lu.code, "requete" in lu.phases),
                                 ("panne_transport", "coupure", None, True))

    def test_resolution_en_echec_vide_ou_trop_lente(self):
        for res in (Resolveur(1, socket.gaierror(-2, "Name or service not known")), Resolveur(None),
                    Resolveur(1, pause=0.3)):
            with self.subTest(erreur=res.erreur, pause=res.pause):
                lu = http.lire(http.Requete("api.example", "/"), resoudre=res, tls=None, delai=S // 5)
                self.assertEqual((lu.statut, lu.sous_type, sorted(lu.phases)),
                                 ("panne_transport", "dns", ["dns"] if res.pause else []))

    def test_connexion_refusee(self):
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]                               # port rendu : rien n'y écoute
        lu = http.lire(http.Requete("api.example", "/"), resoudre=Resolveur(port), tls=None, delai=2 * S)
        self.assertEqual((lu.statut, lu.sous_type, sorted(lu.phases), lu.adresse),
                         ("panne_transport", "connexion", ["dns"], f"127.0.0.1:{port}"))

    def test_poignee_tls_refusee_ou_sans_reponse(self):
        def charabia(conn, recues):
            recues.append(conn.recv(4096))                          # ClientHello
            conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")

        def muet(conn, recues):
            recues.append(conn.recv(4096))
            conn.recv(4096)                                         # jusqu'à la fermeture par le client
        for comportement, sous_type in ((charabia, "tls"), (muet, "delai")):
            with self.subTest(sous_type=sous_type):
                lu, recues, _p = self.lire(comportement, tls=ssl.create_default_context(), delai=S // 2)
                self.assertEqual((lu.statut, lu.sous_type, sorted(lu.phases), recues[0][:1]),
                                 ("panne_transport", sous_type, ["connexion", "dns"], b"\x16"))

    def test_attrape_tout_et_requete_refusee_avant_tout_reseau(self):
        class TlsCasse:
            def wrap_socket(self, *a, **k):
                raise RuntimeError("défaut imprévu")
        lu, recues, _p = self.lire(repondre(b""), tls=TlsCasse())
        self.assertEqual((lu.statut, lu.sous_type, recues), ("panne_transport", "autre", [b""]))
        res = Resolveur(1)
        lu = http.lire(http.Requete("api.example", "/x\r\nX-Injecte: 1"), resoudre=res, tls=None)
        self.assertEqual((lu.statut, lu.sous_type, lu.phases, res.appels), ("panne_transport", "autre", {}, []))

    def test_delai_epuise_entre_deux_phases(self):
        instants = iter([0, 0, 0, 0, S])          # départ, dns, reste avant connexion, connexion, reste avant envoi
        lu = self.lire(repondre(OK7), horloge=lambda: next(instants, S), delai=S)[0]
        self.assertEqual((lu.sous_type, sorted(lu.phases)), ("delai", ["connexion", "dns"]))   # statut contrôlé

    def test_depart_pose_par_la_boucle_et_suivi(self):
        suivi = {"depart": horloge() - S}
        lu = http.lire(http.Requete("api.example", "/"), suivi, resoudre=Resolveur(1), tls=None, delai=S)
        self.assertEqual((lu.statut, lu.sous_type, lu.depart, sorted(suivi)),
                         ("panne_transport", "dns", suivi["depart"], ["adresse", "depart", "phases"]))
