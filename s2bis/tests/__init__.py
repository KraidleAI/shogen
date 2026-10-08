"""Suite de s2bis (CB-0 ; E-C-40) : garde réseau posée à l'import du paquet de tests, avant tout module de test. Une
connexion, un envoi ou une résolution hors de la boucle locale (127.0.0.0/8, ::1, « localhost » ; AF_UNIX permis) lève
ReseauInterdit et s'inscrit dans TENTATIVES. ReseauInterdit dérive de BaseException : un `except Exception` du code
testé ne la masque pas. Un sous-processus pose la garde par `import tests`. Limite : un appel direct à `_socket`."""
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
