"""Client HTTPS par phases (CB-3 ; E-C-03 à E-C-05 ; ADR-0029 §2.9 l.233, l.236). Partie sans réseau. La requête
reprend octet pour octet celle d'urllib en S2 (sources.py l.48-79, ordre des en-têtes mesuré), dont l'en-tête
`Accept-Encoding: identity` (sans lui, tout codage est admis : RFC 9110 §12.5.3). Réponse lue par http.client au
plus juste ; fin du flux avant la fin annoncée : `coupure`, jamais une exception qui sort (PROPOSITION §9, essai 1)."""
import collections
import http.client
import io
import re
import types

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
