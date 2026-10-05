"""CB-10, E-C-27, E-C-28 : client DNS filaire. Octets écrits à la main selon la RFC 1035 (§4.1, pointeur §4.1.4 ;
libellés par od) ; réponses servies en boucle locale à c-ares (Node 22), qui en tire les mêmes valeurs (journal G1)."""
import threading
import unittest

from shogen_s2bis.collecte import dns

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
