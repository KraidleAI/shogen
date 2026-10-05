"""CB-10, E-C-27, E-C-28 : client DNS filaire. Octets écrits à la main selon la RFC 1035 (§4.1, pointeur §4.1.4 ;
libellés par od) ; réponses servies en boucle locale à c-ares (Node 22), qui en tire les mêmes valeurs (journal G1).
CB-11e (C-4 de la G2 de P1-B) : délai sur l'horloge monotone ; MG-23 (C-7). CB-11f : datagramme non apparié ignoré,
adresse non littérale refusée sans envoi (C-2) ; MG-18, MG-19, MG-21, MG-24 (C-7)."""
import socket
import threading
import time
import unittest
from unittest import mock

from shogen_s2bis.collecte import dns
from shogen_s2bis.collecte.lecture import S
from tests.test_http_reseau import Recul

QA = "07 7769746e657373 07 6578616d706c65 00 0001 0001"                         # witness.example., A, IN
Q_SOA = bytes.fromhex("1234 0000 0001 0000 0000 0000 00 0006 0001")              # « . », SOA, sans récursion
Q_A = bytes.fromhex("abcd 0100 0001 0000 0000 0000" + QA)
R_A = bytes.fromhex("abcd 8180 0001 0002 0000 0000" + QA + "c00c 0001 0001 0000003c 0004 c0000201"
                    "c00c 0001 0001 0000012c 0004 c0000202")
R_NX = bytes.fromhex("abcd 8183 0001 0000 0000 0000" + QA)
R_SOA = bytes.fromhex("1234 8400 0001 0001 0000 0000 00 0006 0001 00 0006 0001 00015180 0040"
                      "01 61 0c 726f6f742d73657276657273 03 6e6574 00"                  # a.root-servers.net.
                      "05 6e73746c64 0c 766572697369676e2d677273 03 636f6d 00"           # nstld.verisign-grs.com.
                      "78c3d6b0 00000708 00000384 00093a80 00015180")
QT = QA[:-9] + "0010 0001"                                                      # même nom, TXT
Q_TXT = bytes.fromhex("abcd 0100 0001 0000 0000 0000" + QT)
R_TXT = bytes.fromhex("abcd 8180 0001 0001 0000 0000" + QT + "c00c 0010 0001 0000003c 000c 05 68656c6c6f 05 776f726c64")
WE = "witness.example."
A2 = [[WE, 1, 60, "192.0.2.1"], [WE, 1, 300, "192.0.2.2"]]


def udp(comportement):
    """Serveur UDP sur 127.0.0.1 : reçoit une requête, la consigne, puis `comportement(srv, requete, client)`."""
    srv, recues = socket.socket(socket.AF_INET, socket.SOCK_DGRAM), []
    srv.bind(("127.0.0.1", 0))
    srv.settimeout(5)

    def fil():
        with srv:
            try:
                m, client = srv.recvfrom(4096)
                recues.append(m)
                comportement(srv, m, client)
            except OSError:
                pass
    t = threading.Thread(target=fil, daemon=True)
    t.start()
    return srv.getsockname()[1], recues, t


class Messages(unittest.TestCase):
    def test_requetes_ecrites_a_la_main(self):
        self.assertEqual(dns.requete(0x1234, ".", "SOA", recursion=False), Q_SOA)
        self.assertEqual([dns.requete(0xABCD, n, "A") for n in (WE, "witness.example")], [Q_A, Q_A])
        self.assertEqual(dns.requete(0xABCD, WE, "TXT"), Q_TXT)

    def test_noms_refuses(self):
        for nom in ("a..example", "x" * 64 + ".example", ".".join(["x" * 63] * 4), "é.example", ""):
            with self.subTest(nom=nom[:20]):
                self.assertRaises(ValueError, dns.requete, 1, nom, "A")
        self.assertRaises(ValueError, dns.requete, 1, WE, "MX")                    # type hors de la liste fermée

    def test_analyse_a_soa_txt_nxdomain(self):
        self.assertEqual(dns.analyser(R_A, Q_A), {"rcode": 0, "tc": False, "reponses": A2})
        self.assertEqual(dns.analyser(R_NX, Q_A), {"rcode": 3, "tc": False, "reponses": []})
        self.assertEqual(dns.analyser(R_SOA, Q_SOA)["reponses"], [[".", 6, 86400, [
            "a.root-servers.net.", "nstld.verisign-grs.com.", 2026100400, 1800, 900, 604800, 86400]]])
        self.assertEqual(dns.analyser(R_TXT, Q_TXT)["reponses"], [[WE, 16, 60, ["hello", "world"]]])
        self.assertEqual(dns.analyser(R_A[:2] + bytes([0x83]) + R_A[3:], Q_A)["tc"], True)

    def test_txt_hors_ascii_lu_en_latin1(self):
        """MG-18 : une chaîne TXT hors ASCII se lit en latin-1 (octet 0xE9 : U+00E9), sans refus."""
        r = dns.analyser(R_TXT[:-10] + bytes([0xE9]) + R_TXT[-9:], Q_TXT)
        self.assertEqual(r["reponses"], [[WE, 16, 60, ["h" + chr(0xE9) + "llo", "world"]]])

    def test_types_d_etiquette_reserves_refuses(self):
        """MG-19 : un octet d'étiquette de 0x40 à 0xBF (combinaisons 01 et 10 réservées, RFC 1035 §4.1.4) est refusé,
        même quand assez d'octets le suivent pour le lire comme une longueur (0x41 : 65 octets « a »)."""
        rr = bytes([0x41]) + b"a" * 65 + bytes.fromhex("00 0001 0001 0000003c 0004 c0000201")
        self.assertRaises(dns.Forme, dns.analyser, R_A[:7] + bytes([1]) + R_A[8:len(Q_A)] + rr, Q_A)

    def test_reponses_mal_formees_refusees_en_temps_borne(self):
        n, refus = len(Q_A), []

        def essayer(k, q, m):
            try:
                dns.analyser(m, q)
            except dns.Forme:
                refus.append(k)
        cas = [(Q_A, R_A[:n] + bytes.fromhex(f"c0{n:02x}") + R_A[n + 2:]),          # pointeur sur lui-même
               (Q_A, R_A[:n] + bytes.fromhex(f"c0{n + 2:02x}") + R_A[n + 2:]),      # pointeur en avant
               (Q_A, R_A[:-2]), (Q_A, R_A[:-6] + bytes.fromhex("0005c000020201")),  # tronquée ; A de 5 octets
               (Q_A, R_A[:2] + bytes([0x01]) + R_A[3:]), (Q_A, R_TXT),             # pas une réponse ; autre question
               (Q_A, bytes([0xAB, 0xCE]) + R_A[2:]), (Q_A, R_A[:n] + bytes([0x40]) + R_A[n + 1:]),
               (Q_TXT, R_TXT[:-14] + bytes.fromhex("000b") + R_TXT[-12:]),         # chaîne TXT qui déborde
               (Q_SOA, R_SOA[:26] + bytes.fromhex("0041") + R_SOA[28:] + bytes(1))]  # SOA suivi d'un octet
        fils = [threading.Thread(target=essayer, args=(k, *c), daemon=True) for k, c in enumerate(cas)]
        for f in fils:
            f.start()
            f.join(2)                                                   # une boucle de pointeurs pendrait ici
        self.assertEqual(([f.is_alive() for f in fils], sorted(refus)), ([False] * len(cas), list(range(len(cas)))))


class Interroger(unittest.TestCase):
    def test_intrus_ignores_reponse_retenue(self):
        def comportement(srv, requete, client):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as autre:
                autre.sendto(requete[:2] + R_NX[2:], client)                # autre source : ignoré
            srv.sendto(bytes([requete[0] ^ 1]) + R_NX[1:], client)           # autre identifiant : ignoré
            srv.sendto(requete[:2] + R_A[2:], client)
        port, recues, fil = udp(comportement)
        r = dns.interroger("127.0.0.1", WE, "A", delai=S, port=port, ident=0xABCD)
        fil.join(5)
        self.assertEqual((recues, r["statut"], r["rcode"], r["reponses"]), ([Q_A], "reponse", 0, A2))
        self.assertTrue(type(r["debut"]) is int and r["debut"] <= r["fin"] < r["debut"] + S // 2)

    def test_delai_reseau_forme_et_identifiant_aleatoire(self):
        resultats, recues = [], []

        def muets():
            for _ in range(3):
                port, vues, fil = udp(lambda *a: None)                     # serveur muet
                resultats.append(dns.interroger("127.0.0.1", ".", "SOA", recursion=False, delai=S // 5, port=port))
                fil.join(5)
                recues.extend(vues)
        f = threading.Thread(target=muets, daemon=True)
        f.start()
        f.join(5)                                                       # une attente sans délai pendrait ici
        self.assertEqual([(r["statut"], r["rcode"], r["reponses"]) for r in resultats], [("delai", None, None)] * 3)
        self.assertTrue(all(S // 5 <= r["fin"] - r["debut"] < 3 * S // 10 for r in resultats), resultats)
        self.assertGreater(len({m[:2] for m in recues}), 1)
        self.assertEqual([m[2:] for m in recues], [Q_SOA[2:]] * 3)
        self.assertEqual(dns.interroger("127.0.0.1", ".", "SOA", port=0)["statut"], "reseau")
        self.assertEqual(dns.interroger("127.0.0.1", "a..b", "A", port=1)["statut"], "forme")

    def test_delai_sur_l_horloge_monotone_malgre_un_recul(self):
        """C-4 (S-C2 de la G2) : datagrammes d'un autre identifiant toutes les 0,05 s, horloge murale reculée de 3 s
        après 0,1 s : le délai de 0,3 s, compté sur l'horloge monotone, tient."""
        def bruit(srv, requete, client):
            for _ in range(20):
                srv.sendto(bytes([requete[0] ^ 1]) + requete[1:], client)
                time.sleep(0.05)
        port, _r, fil = udp(bruit)
        t = time.monotonic()
        r = dns.interroger("127.0.0.1", WE, "A", delai=3 * S // 10, port=port, horloge=Recul(3 * S, S // 10))
        duree = time.monotonic() - t
        fil.join(5)
        self.assertEqual(r["statut"], "delai")
        self.assertTrue(0.3 <= duree < 1, duree)

    def test_attente_close_au_delai_apres_un_datagramme_etranger(self):
        """MG-23 : un datagramme étranger reçu, puis le délai épuisé (horloge monotone injectée) : l'attente s'arrête
        là, statut `delai`, sans un tour de plus."""
        port, _r, fil = udp(lambda srv, requete, client: srv.sendto(bytes([requete[0] ^ 1]) + requete[1:], client))
        instants = iter([0, 0])                                         # début, premier tour ; puis délai dépassé
        r = dns.interroger("127.0.0.1", WE, "A", delai=S, port=port, monotone=lambda: next(instants, S + 1))
        fil.join(5)
        self.assertEqual(r["statut"], "delai")

    def test_datagrammes_non_apparies_ignores(self):
        """C-2 (a) : de la bonne source, avec le bon identifiant, l'écho de la requête (QR nul, S-D1), la réponse à une
        autre question (S-D2), une réponse à deux questions (MG-21) et un datagramme de deux octets sont ignorés :
        l'attente continue jusqu'à la réponse appariée, retenue."""
        def comportement(srv, requete, client):
            for m in (requete, requete[:2] + R_NX[2:12] + Q_TXT[12:], requete[:2] + R_NX[2:5] + bytes([2]) + R_NX[6:],
                      requete[:2], requete[:2] + R_A[2:]):
                srv.sendto(m, client)
        port, _r, fil = udp(comportement)
        r = dns.interroger("127.0.0.1", WE, "A", delai=S, port=port)
        fil.join(5)
        self.assertEqual((r["statut"], r["rcode"], r["reponses"]), ("reponse", 0, A2))

    def test_adresse_non_litterale_refusee_sans_envoi(self):
        """C-2 (b) : une adresse qui n'est pas une IPv4 littérale canonique (« 127.1 », S-D7 ; None, S-D8 ;
        « localhost », S-D9 ; zéro de tête ; espace ; entier) donne `forme`, sans exception, résolution ni envoi."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as srv:
            srv.bind(("127.0.0.1", 0))
            for adresse in ("127.1", None, "localhost", "127.0.0.01", " 127.0.0.1", 2130706433):
                with self.subTest(adresse=adresse):
                    r = dns.interroger(adresse, WE, "A", delai=S // 10, port=srv.getsockname()[1])
                    self.assertEqual((r["statut"], r["rcode"]), ("forme", None))
            srv.setblocking(False)
            self.assertRaises(BlockingIOError, srv.recvfrom, 4096)         # aucune requête n'est partie

    def test_identifiant_tire_sur_16_bits(self):
        """MG-24 : l'identifiant est tiré par `secrets.randbelow(65536)` et porté tel quel par la requête."""
        port, recues, fil = udp(lambda *a: None)
        with mock.patch.object(dns.secrets, "randbelow", return_value=0xBEEF) as tirage:
            dns.interroger("127.0.0.1", WE, "A", delai=S // 10, port=port)
        fil.join(5)
        self.assertEqual((tirage.call_args_list, recues[0][:2]), ([mock.call(1 << 16)], bytes([0xBE, 0xEF])))
