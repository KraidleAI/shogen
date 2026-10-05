"""Client HTTPS par phases (CB-3 ; E-C-03 à E-C-05 ; ADR-0029 §2.9 l.233, l.236) ; `lire` ne lève jamais. La requête
reprend octet pour octet celle d'urllib en S2 (sources.py l.48-79, ordre des en-têtes mesuré), dont l'en-tête
`Accept-Encoding: identity` (sans lui, tout codage est admis : RFC 9110 §12.5.3). Réponse lue par http.client au
plus juste ; fin du flux avant la fin annoncée : `coupure`, jamais une exception qui sort (PROPOSITION §9, essai 1).
Contexte TLS armé comme celui d'urllib en S2 (http.client sans contexte : ALPN `http/1.1`, authentification après
poignée annoncée ; Python 3.10 l.1441-1448, 3.12 l.824-835) : même ClientHello qu'en S2 (C-3 de la G2 de P1-B)."""
import collections
import http.client
import io
import re
import socket
import ssl
import types

from shogen_s2bis.collecte.lecture import S, Lecture, horloge, monotone

DELAI = 10 * S                                                      # délai global d'une lecture (ADR-0029 l.233)
CONTEXTE = ssl.create_default_context()                             # certificats vérifiés, nom d'hôte contrôlé
CONTEXTE.set_alpn_protocols(["http/1.1"])                           # comme urllib en S2 (C-3) : ALPN http/1.1 et
CONTEXTE.post_handshake_auth = True                                 # authentification après poignée (TLS 1.3)
PLAFOND = 1 << 20                    # octets reçus au plus, en-têtes compris (l'enregistrement tient sous la borne)
UA = "Mozilla/5.0 (Shogen-S2-harness; +https://github.com/KraidleAI/shogen)"    # S2, sources.py l.40 (continuité)
Requete = collections.namedtuple("Requete", "hote chemin port methode corps", defaults=(443, "GET", None))


class Panne(Exception):
    """Défaut d'une phase de la lecture ; `sous_type` : dns, connexion, tls, delai, coupure ou autre."""
    def __init__(self, sous_type):
        super().__init__(sous_type)
        self.sous_type = sous_type


def octets(req):
    """Octets de la requête ; hôte, chemin ou méthode vide ou hors ASCII imprimable sans espace : panne `autre`."""
    if not all(re.fullmatch("[!-~]+", x) for x in (req.hote, req.chemin, req.methode)):
        raise Panne("autre")
    tete = [f"{req.methode} {req.chemin} HTTP/1.1", "Accept-Encoding: identity"]
    tete += [] if req.corps is None else [f"Content-Length: {len(req.corps)}"]
    tete += [f"Host: {req.hote}" + ("" if req.port == 443 else f":{req.port}"), f"User-Agent: {UA}",
             "Accept: application/json"]
    tete += ([] if req.corps is None else ["Content-Type: application/json"]) + ["Connection: close"]
    return ("\r\n".join(tete) + "\r\n\r\n").encode("ascii") + (req.corps or b"")


class _Flux(io.RawIOBase):
    """Flux brut : `recevoir(tampon)` écrit dans le tampon et rend le nombre d'octets (0 : fin du flux, notée)."""
    def __init__(self, recevoir, plafond):
        super().__init__()
        self.recevoir, self.reste, self.fin = recevoir, plafond, False

    def readable(self):
        return True

    def readinto(self, tampon):
        n = self.recevoir(tampon)
        self.reste, self.fin = self.reste - n, self.fin or n == 0
        if self.reste < 0:
            raise Panne("autre")
        return n


def analyser(recevoir, plafond=PLAFOND):
    """(code, corps) de la réponse reçue. Fin du flux avant la fin des en-têtes ou du corps annoncé : `coupure` ;
    réponse illisible (sans fin de flux : taille de bloc illisible) ou plus de `plafond` octets reçus : `autre`.
    Une Panne levée par `recevoir` (délai épuisé, défaut de la connexion) passe telle quelle."""
    brut = _Flux(recevoir, plafond)
    r = http.client.HTTPResponse(types.SimpleNamespace(makefile=lambda _mode: io.BufferedReader(brut)))
    try:
        r.begin()
        if brut.fin:
            raise Panne("coupure")                                   # en-têtes interrompus par la fin du flux
        return r.status, r.read()
    except (http.client.IncompleteRead, http.client.RemoteDisconnected):
        raise Panne("coupure" if brut.fin else "autre") from None
    except (http.client.HTTPException, ValueError):
        raise Panne("autre") from None
    finally:
        r.close()                                                   # flux fermé aussi après un refus


def lire(req, suivi=None, delai=DELAI, resoudre=None, tls=CONTEXTE, horloge=horloge, plafond=PLAFOND,
         monotone=monotone):
    """Lecture de `req`, sans jamais lever (E-C-03) ; code autre que 200 : `panne_http`, sans suivre de redirection.
    `suivi` (partagé avec la boucle) reçoit `depart` (gardé s'il est posé), `phases` et `adresse` au fil de l'eau.
    `resoudre` (getaddrinfo injectable, en AF_INET) ne se borne pas : délai épuisé pendant la résolution, `dns` ;
    l'échéance de la boucle borne le tout (PROPOSITION §9, essai 2). `tls` None : TCP nu (serveurs des tests). Délai
    sur l'horloge `monotone`, instants sur l'horloge murale (C-4) ; il court depuis `suivi["monotone"]`, départ que
    la boucle relève sur l'horloge monotone (CB-18b), sinon depuis le début de la lecture."""
    suivi = {} if suivi is None else suivi
    phases, depart, socks = suivi.setdefault("phases", {}), suivi.setdefault("depart", horloge()), []
    fin = suivi.get("monotone", monotone()) + delai

    def borner(s, defaut, operation, *args):
        """`operation(*args)` sous le temps qui reste avant `fin` (délai global) ; épuisé : delai ; OSError : defaut."""
        try:
            reste = fin - monotone()
            if reste <= 0:
                raise TimeoutError
            s.settimeout(reste / S)
            return operation(*args)
        except OSError as e:
            raise Panne("delai" if isinstance(e, TimeoutError) else defaut) from None

    try:
        requete = octets(req)
        try:
            adresses = (resoudre or socket.getaddrinfo)(req.hote, req.port, socket.AF_INET, socket.SOCK_STREAM)
            ip, port = adresses[0][4][:2]
        except Exception:
            raise Panne("dns") from None
        phases["dns"], suivi["adresse"] = horloge(), f"{ip}:{port}"
        if monotone() >= fin:
            raise Panne("dns")                                      # délai épuisé pendant la résolution
        socks.append(s := socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        borner(s, "connexion", s.connect, (ip, port))
        phases["connexion"] = horloge()
        if tls is not None:
            socks.append(s := tls.wrap_socket(s, server_hostname=req.hote, do_handshake_on_connect=False))
            borner(s, "tls", s.do_handshake)
            phases["tls"] = horloge()
        borner(s, "coupure", s.sendall, requete)
        phases["requete"] = horloge()
        code, corps = analyser(lambda tampon: borner(s, "coupure", s.recv_into, tampon), plafond)
        phases["corps"] = horloge()
        return Lecture("ok" if code == 200 else "panne_http", depart, horloge(), phases, suivi["adresse"], code=code,
                       octets=corps)
    except Exception as e:                                          # attrape-tout typé
        return Lecture("panne_transport", depart, horloge(), phases, suivi.get("adresse"),
                       sous_type=e.sous_type if isinstance(e, Panne) else "autre")
    finally:
        for x in socks:
            x.close()
