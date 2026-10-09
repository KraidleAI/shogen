"""CB-0, E-C-40, E-C-41 : la garde réseau de tests/__init__.py refuse toute sortie hors boucle locale, même sous un
attrape-tout, et laisse passer la boucle locale. Adresses de documentation (192.0.2.0/24, RFC 5737) et domaine
réservé (.invalid, RFC 2606) : un mutant sans garde n'atteint aucun service réel."""
import os
import socket
import subprocess
import sys
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
                          lambda: socket.create_connection(("192.0.2.1", 443), timeout=1),
                          lambda: s.connect_ex(("192.0.2.1", 443))):                    # C-5 (M-26 de la G2)
                self.assertRaises(tests.ReseauInterdit, appel)
        self.assertEqual([h for _n, h in tests.TENTATIVES[n:]],
                         ["192.0.2.1", "192.0.2.1", "example.invalid", "example.invalid", "192.0.2.1", "192.0.2.1"])

    def test_boucle_locale_permise(self):
        with socket.socket() as srv:
            srv.bind(("127.0.0.1", 0))
            srv.listen()
            socket.create_connection(srv.getsockname(), timeout=1).close()

    def test_mandataires_purges(self):
        """SHOGEN-TESTS-GARDE-MANDATAIRE-1 : un mandataire sur la boucle locale (HTTPS_PROXY=http://127.0.0.1:…) ferait
        sortir urllib par la boucle locale, que la garde admet. Vérifié hors de l'environnement courant (le job peut
        tourner sans mandataire) : un sous-processus pose dix variables de mandataire fictives (majuscules, minuscules,
        casse de titre, casse mêlée pour chacun des trois schémas ; urllib lit toute casse du préfixe et du suffixe),
        importe tests et lit urllib.request.getproxies() : aucune clé http, https ni all, et l'environnement du
        processus n'en garde aucune."""
        noms = ("HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy", "Https_Proxy",
                "hTtP_pRoXy", "hTtPs_PrOxY", "aLl_pRoXy")
        code = ("import os, tests, urllib.request as u; print(sorted({'http', 'https', 'all'} & set(u.getproxies())),"
                " sorted(k for k in os.environ if k.lower() in ('http_proxy', 'https_proxy', 'all_proxy')))")
        ici = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        r = subprocess.run([sys.executable, "-B", "-c", code], cwd=ici, capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=ici, **dict.fromkeys(noms, "http://127.0.0.1:9")))
        self.assertEqual((r.returncode, r.stdout), (0, "[] []" + chr(10)), r.stderr)
