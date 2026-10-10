"""Lot DETTES-T5 (2026-10-09 ; ADR-0028 annexe B.4, SHOGEN-CI-S2-FORGE-1 (d)) : la garde réseau de tests/__init__.py,
forme de s2bis/tests/__init__.py, refuse toute sortie hors boucle locale, même sous un attrape-tout, laisse passer la
boucle locale et retire les variables de mandataire. Adresses de documentation (192.0.2.0/24, RFC 5737) et domaine
réservé (.invalid, RFC 2606) : un mutant sans garde n'atteint aucun service réel."""
import os
import socket
import subprocess
import sys
import unittest

import tests


def levee(appel):
    """Nom de la classe de l'exception levée par `appel`, None s'il n'en lève aucune ; ReseauInterdit dérive de
    BaseException, d'où la capture large, bornée à ce relevé."""
    try:
        appel()
    except BaseException as e:
        return type(e).__name__
    return None


class GardeReseau(unittest.TestCase):
    def test_sorties_refusees_et_inscrites(self):
        tentatives = getattr(tests, "TENTATIVES", [])
        n = len(tentatives)

        def attrape_tout():
            try:
                socket.getaddrinfo("example.invalid", 443)
            except Exception:
                pass
        with socket.socket() as s, socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as u:
            s.settimeout(1)
            appels = (lambda: s.connect(("192.0.2.1", 443)), lambda: s.connect_ex(("192.0.2.1", 443)),
                      lambda: u.sendto(b"x", ("192.0.2.1", 53)), lambda: socket.gethostbyname("example.invalid"),
                      lambda: socket.gethostbyname_ex("example.invalid"), lambda: socket.gethostbyaddr("192.0.2.1"),
                      attrape_tout, lambda: socket.create_connection(("192.0.2.1", 443), timeout=1))
            self.assertEqual([levee(a) for a in appels], ["ReseauInterdit"] * len(appels))
        self.assertEqual([h for _n, h in tentatives[n:]],
                         ["192.0.2.1"] * 3 + ["example.invalid"] * 2 + ["192.0.2.1", "example.invalid", "192.0.2.1"])

    def test_resolution_par_mot_cle_et_getnameinfo(self):
        """Contre-contrôle du lot (R-3) et adjudication C-11 : getaddrinfo, l'hôte passé par mot-clé, et getnameinfo
        hors de la boucle locale refusés et inscrits ; boucle locale (littéraux de 127.0.0.0/8 et de ::1) admise."""
        tentatives = getattr(tests, "TENTATIVES", [])
        n, num = len(tentatives), socket.NI_NUMERICHOST | socket.NI_NUMERICSERV
        appels = (lambda: socket.getaddrinfo(host="example.invalid", port=443),
                  lambda: socket.getnameinfo(("192.0.2.1", 80), 0),
                  lambda: socket.getnameinfo(("2001:db8::1", 80, 0, 0), 0))
        self.assertEqual([levee(a) for a in appels], ["ReseauInterdit"] * 3)
        self.assertEqual([h for _n, h in tentatives[n:]], ["example.invalid", "192.0.2.1", "2001:db8::1"])
        self.assertEqual([levee(lambda: socket.getaddrinfo(host="127.0.0.1", port=80)),
                          levee(lambda: socket.getnameinfo(("127.0.0.1", 80), num)),
                          levee(lambda: socket.getnameinfo(("::1", 80, 0, 0), num))], [None] * 3)

    def test_boucle_locale_permise(self):
        with socket.socket() as srv:
            srv.bind(("127.0.0.1", 0))
            srv.listen()
            self.assertEqual([levee(lambda: socket.create_connection(srv.getsockname(), timeout=1).close()),
                              levee(lambda: socket.getaddrinfo("127.0.0.1", 80))], [None, None])

    def test_mandataires_purges(self):
        """Un mandataire sur la boucle locale (HTTPS_PROXY=http://127.0.0.1:…) ferait sortir urllib par la boucle
        locale, que la garde admet. Vérifié hors de l'environnement courant (le job peut tourner sans mandataire) : un
        sous-processus pose dix variables de mandataire fictives (majuscules, minuscules, casse de titre, casse mêlée
        pour chacun des trois schémas), importe tests et lit urllib.request.getproxies() : aucune clé http, https ni
        all, et l'environnement du processus n'en garde aucune."""
        noms = ("HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy", "Https_Proxy",
                "hTtP_pRoXy", "hTtPs_PrOxY", "aLl_pRoXy")
        code = ("import os, tests, urllib.request as u; print(sorted({'http', 'https', 'all'} & set(u.getproxies())),"
                " sorted(k for k in os.environ if k.lower() in ('http_proxy', 'https_proxy', 'all_proxy')))")
        ici = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        r = subprocess.run([sys.executable, "-B", "-c", code], cwd=ici, capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=ici, **dict.fromkeys(noms, "http://127.0.0.1:9")))
        self.assertEqual((r.returncode, r.stdout), (0, "[] []" + chr(10)), r.stderr)
