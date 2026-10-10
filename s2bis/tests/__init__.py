"""Suite de s2bis (CB-0 ; E-C-40) : garde réseau posée à l'import du paquet de tests, avant tout module de test. Une
connexion (connect, connect_ex), un envoi (sendto) ou une résolution (getaddrinfo, l'hôte positionnel ou `host=`,
gethostbyname, gethostbyname_ex, gethostbyaddr, getnameinfo) hors de la boucle locale (127.0.0.0/8, ::1,
« localhost » ; AF_UNIX permis) lève ReseauInterdit et s'inscrit dans TENTATIVES (`host=` et getnameinfo : lot
DETTES-T5, adjudication C-11). ReseauInterdit dérive de BaseException : un `except Exception` du code testé ne la masque
pas. Un sous-processus pose la garde par `import tests`. Limites : un appel direct à `_socket` ; un envoi par `sendmsg`
vers une adresse, non gardé (lot DETTES-T5, 2026-10-09 : relecture G2, C-6, et adjudication C-9 ; documentaire).
SHOGEN-TESTS-GARDE-MANDATAIRE-1 : les variables de mandataire (http_proxy, https_proxy, all_proxy, toutes casses) sont
retirées de l'environnement, et de celui des sous-processus, avant la garde : un mandataire sur la boucle locale
(HTTPS_PROXY=http://127.0.0.1:…) ferait sortir urllib par la boucle locale, que la garde admet."""
import ipaddress
import os
import socket

TENTATIVES = []
for _v in [k for k in os.environ if k.lower() in ("http_proxy", "https_proxy", "all_proxy")]:
    del os.environ[_v]


class ReseauInterdit(BaseException):
    pass


def _local(h):
    try:
        return h in (None, "localhost") or ipaddress.ip_address(h).is_loopback
    except ValueError:
        return False


def _garde(nom, original, hote):
    def garde(*a, **k):
        h = hote(a, k)
        if not _local(h):
            TENTATIVES.append((nom, h))
            raise ReseauInterdit(f"{nom} vers {h!r} : réseau interdit aux tests")
        return original(*a, **k)
    return garde


for _n in ("connect", "connect_ex", "sendto"):
    setattr(socket.socket, _n, _garde(_n, getattr(socket.socket, _n),
                                      lambda a, k: "localhost" if a[0].family == socket.AF_UNIX else a[-1][0]))
for _n in ("getaddrinfo", "gethostbyname", "gethostbyname_ex", "gethostbyaddr"):      # hôte positionnel ou host=
    setattr(socket, _n, _garde(_n, getattr(socket, _n), lambda a, k: a[0] if a else k.get("host")))
socket.getnameinfo = _garde("getnameinfo", socket.getnameinfo,      # hôte de sockaddr ; vide : l'appel d'origine juge
                            lambda a, k: (tuple(a[0] if a else k.get("sockaddr") or ()) + (None,))[0])
