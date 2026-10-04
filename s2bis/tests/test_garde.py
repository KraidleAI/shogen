"""CB-0, E-C-40, E-C-41 : la garde réseau de tests/__init__.py refuse toute sortie hors boucle locale, même sous un
attrape-tout, et laisse passer la boucle locale. Adresses de documentation (192.0.2.0/24, RFC 5737) et domaine
réservé (.invalid, RFC 2606) : un mutant sans garde n'atteint aucun service réel."""
import socket
import unittest

import tests


class Garde(unittest.TestCase):
    def test_sorties_refusees_et_inscrites(self):
        n = len(tests.TENTATIVES)

        def attrape_tout():
            try:
                socket.getaddrinfo("example.invalid", 443)
            except Exception:
                pass
        with socket.socket() as s, socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as u:
            s.settimeout(1)
            for appel in (lambda: s.connect(("192.0.2.1", 443)), lambda: u.sendto(b"x", ("192.0.2.1", 53)),
                          lambda: socket.gethostbyname("example.invalid"), attrape_tout,
                          lambda: socket.create_connection(("192.0.2.1", 443), timeout=1)):
                self.assertRaises(tests.ReseauInterdit, appel)
        self.assertEqual([h for _n, h in tests.TENTATIVES[n:]],
                         ["192.0.2.1", "192.0.2.1", "example.invalid", "example.invalid", "192.0.2.1"])

    def test_boucle_locale_permise(self):
        with socket.socket() as srv:
            srv.bind(("127.0.0.1", 0))
            srv.listen()
            socket.create_connection(srv.getsockname(), timeout=1).close()
