"""Tests du lot CALIB-ACTIFS, sur fixtures synthétiques seulement (E-CA-05, E-CA-31 ; aucun historique réel, aucun
journal), depuis scripts/calib-actifs : env -u SHOGEN_S2_CAMPAGNE_CONTROL python3 -B -m unittest discover -s tests -t .
Garde réseau posée à l'import du paquet de tests (forme de s2bis/tests/__init__.py) : une connexion, un envoi ou une
résolution hors de la boucle locale lève ReseauInterdit (BaseException) ; le serveur local des tests d'acquisition
écoute sur 127.0.0.1."""
import ipaddress
import socket

TENTATIVES = []


class ReseauInterdit(BaseException):
    pass


def _local(h):
    try:
        return h in (None, "localhost") or ipaddress.ip_address(h).is_loopback
    except ValueError:
        return False


def _garde(nom, original, hote):
    def garde(*a, **k):
        if not _local(hote(a)):
            TENTATIVES.append((nom, hote(a)))
            raise ReseauInterdit(f"{nom} vers {hote(a)!r} : réseau interdit aux tests")
        return original(*a, **k)
    return garde


for _n in ("connect", "connect_ex", "sendto"):
    setattr(socket.socket, _n, _garde(_n, getattr(socket.socket, _n),
                                      lambda a: "localhost" if a[0].family == socket.AF_UNIX else a[-1][0]))
for _n in ("getaddrinfo", "gethostbyname", "gethostbyname_ex", "gethostbyaddr"):
    setattr(socket, _n, _garde(_n, getattr(socket, _n), lambda a: a[0] if a else None))
