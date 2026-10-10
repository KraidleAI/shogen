"""Suite du harnais S2. SHOGEN-TESTS-TMP-1 (ADR-0028, lot B0) : tout `mkdtemp` de la suite est
rangé sous un dossier unique, retiré à la fin du processus (0 entrée laissée dans TMP).
Lot DETTES-T5 (2026-10-09 ; SHOGEN-CI-S2-FORGE-1 (d), ADR-0028 annexe B.4) : garde réseau de s2bis/tests/__init__.py,
même forme, posée à l'import du paquet de tests, avant tout module de test, et donc dans le job s2-harness-unittest.
Une connexion (connect, connect_ex), un envoi (sendto) ou une résolution (getaddrinfo, gethostbyname,
gethostbyname_ex, gethostbyaddr) hors de la boucle locale (127.0.0.0/8, ::1, « localhost » ; AF_UNIX permis) lève
ReseauInterdit et s'inscrit dans TENTATIVES ; ReseauInterdit dérive de BaseException : un `except Exception` du code
testé ne la masque pas. Les variables de mandataire (http_proxy, https_proxy, all_proxy, toutes casses) sont
retirées de l'environnement, et de celui des sous-processus, avant la garde. Limites : un appel direct à `_socket` ;
un envoi par `sendmsg` vers une adresse, non gardé, comme dans s2bis/tests/__init__.py (relecture G2 du lot, C-6) ;
un sous-processus Python n'a la garde que s'il importe tests."""
import atexit
import ipaddress
import os
import shutil
import socket
import sys
import tempfile

tempfile.tempdir = tempfile.mkdtemp(prefix="s2suite_")
atexit.register(shutil.rmtree, tempfile.tempdir)
sys.dont_write_bytecode = True                  # E-4 (G2 B0) : aucun __pycache__ dans l'arbre,
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"     # ni par les sous-processus (cli(), chemin servi)

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
