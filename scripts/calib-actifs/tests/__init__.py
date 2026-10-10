"""Tests du lot CALIB-ACTIFS, sur fixtures synthétiques seulement (E-CA-05, E-CA-31 ; aucun historique réel, aucun
journal), depuis scripts/calib-actifs : env -u SHOGEN_S2_CAMPAGNE_CONTROL python3 -B -m unittest discover -s tests -t .
Garde réseau posée à l'import du paquet de tests (bloc égal octet pour octet à celui de s2bis/tests/__init__.py, de
« TENTATIVES = [] » à la fin) : une connexion (connect, connect_ex), un envoi (sendto) ou une résolution (getaddrinfo,
l'hôte positionnel ou `host=`, gethostbyname, gethostbyname_ex, gethostbyaddr, getnameinfo) hors de la boucle locale
lève ReseauInterdit (BaseException) ; le serveur local des tests d'acquisition écoute sur 127.0.0.1. Limites : un appel
direct à `_socket` ; un envoi par `sendmsg` vers une adresse ; un sous-processus n'a la garde que s'il importe tests.
Une forme d'appel invalide est laissée à l'appel d'origine (TypeError). Bloc aligné sur C-11 du lot DETTES-T5
(contre-contrôle, passe 2).
Les variables de mandataire sont retirées de l'environnement (et de celui des sous-processus) :
un mandataire sur la boucle locale (HTTPS_PROXY=127.0.0.1:…) ferait passer toute requête sous la garde."""
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
# Hôte positionnel, ou host= pour getaddrinfo seul (les fonctions C n'admettent aucun mot-clé) ; getnameinfo : hôte d'un
# sockaddr en tuple, sans mot-clé. Toute autre forme est laissée à l'appel d'origine, qui lève TypeError : rien n'est
# inscrit (contre-contrôle du lot, passe 2).
for _n in ("getaddrinfo", "gethostbyname", "gethostbyname_ex", "gethostbyaddr"):
    setattr(socket, _n, _garde(_n, getattr(socket, _n),
                               lambda a, k, n=_n: a[0] if a else k.get("host") if n == "getaddrinfo" else None))
socket.getnameinfo = _garde("getnameinfo", socket.getnameinfo,
                            lambda a, k: a[0][0] if a and not k and isinstance(a[0], tuple) and a[0] else None)
