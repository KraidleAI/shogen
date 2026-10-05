"""Client DNS filaire (CB-10 ; E-C-27, E-C-28 ; ADR-0029 §2.3, D-4 et D-5), format RFC 1035 (§4.1) : octets d'une
requête (en-tête de 12 octets, une question A, SOA ou TXT de classe IN) ; analyse d'une réponse, retenue seulement si
elle porte le même identifiant, le bit QR et la même question ; données prêtes pour le journal (rcode, drapeau TC,
réponses avec leur TTL). Le jugement (D-4, D-5) se fait au recalcul. `interroger` (CB-10b) : une requête en UDP vers une
adresse IPv4 littérale, sans aucune résolution, identifiant tiré au hasard ; tout datagramme qui ne vient pas de cette
adresse et de ce port, ou d'un autre identifiant, est ignoré ; ne lève jamais (instants en microsecondes)."""
import secrets
import socket
import struct

from shogen_s2bis.collecte.lecture import S, horloge, monotone

TYPES = {"A": 1, "SOA": 6, "TXT": 16}


class Forme(ValueError):
    """Message DNS mal formé, ou qui ne répond pas à la requête."""


def requete(ident, nom, qtype, recursion=True):
    """Octets de la requête ; `nom` en ASCII, étiquettes de 1 à 63 octets, 255 octets au plus ; « . » : la racine."""
    etiquettes = [] if nom == "." else [e.encode("ascii") for e in nom.removesuffix(".").split(".")]
    if qtype not in TYPES or not all(0 < len(e) < 64 for e in etiquettes) or sum(len(e) + 1 for e in etiquettes) > 254:
        raise ValueError(f"requête DNS invalide : {nom!r}, {qtype!r}")
    return (struct.pack(">6H", ident, 0x0100 if recursion else 0, 1, 0, 0, 0) +
            b"".join(bytes([len(e)]) + e for e in etiquettes) + bytes(1) + struct.pack(">2H", TYPES[qtype], 1))


def _nom(m, i):
    """(nom, position qui suit) ; chaque pointeur (§4.1.4) vise avant le début du segment courant : pas de boucle."""
    etiquettes, suite, borne = [], None, i
    while m[i]:
        if m[i] >= 0xC0:
            cible = (m[i] & 0x3F) << 8 | m[i + 1]
            if cible >= borne:
                raise Forme("pointeur")
            suite, i, borne = suite or i + 2, cible, cible
        elif m[i] < 0x40 and i + 1 + m[i] <= len(m):
            etiquettes.append(m[i + 1:i + 1 + m[i]].decode("ascii"))
            i += 1 + m[i]
        else:
            raise Forme("étiquette")
    return ".".join(etiquettes) + ".", suite or i + 1


def _donnees(m, t, i, fin):
    """Données : A, adresse ; TXT, chaînes (latin-1) ; SOA, [mname, rname, serial, refresh, retry, expire, minimum]."""
    if t == 6:
        mname, i = _nom(m, i)
        rname, i = _nom(m, i)
        return [mname, rname, *struct.unpack(">5I", m[i:fin])]          # struct.error si la taille diffère
    if t == 16:
        chaines = []
        while i < fin:
            chaines.append(m[i + 1:i + 1 + m[i]].decode("latin-1"))
            i += 1 + m[i]
        if i == fin:
            return chaines
    elif t != 1:
        return None
    elif fin - i == 4:
        return socket.inet_ntoa(m[i:fin])
    raise Forme(f"données de type {t}")


def analyser(m, q):
    """{rcode, tc, reponses : [nom, type, ttl, données]} ; Forme si `m` est mal formé ou ne répond pas à `q`."""
    try:
        ident, drapeaux, qd, an = struct.unpack(">4H", m[:8])
        if m[:2] != q[:2] or not drapeaux & 0x8000 or qd != 1 or m[12:len(q)].lower() != q[12:].lower():
            raise Forme("pas une réponse à la requête")
        reponses, i = [], len(q)
        for _ in range(an):
            nom, i = _nom(m, i)
            t, _c, ttl, n = struct.unpack(">HHIH", m[i:i + 10])
            if i + 10 + n > len(m):
                raise Forme("tronquée")
            reponses.append([nom, t, ttl, _donnees(m, t, i + 10, i + 10 + n)])
            i += 10 + n
        return {"rcode": drapeaux & 0x0F, "tc": bool(drapeaux & 0x0200), "reponses": reponses}
    except (IndexError, ValueError, struct.error) as e:                # UnicodeDecodeError et Forme compris
        raise Forme(str(e)) from None


def interroger(adresse, nom, qtype, recursion=True, delai=2 * S, port=53, horloge=horloge, ident=None,
               monotone=monotone):
    """Une requête vers `adresse`:`port`, réponse attendue `delai` au plus, compté sur l'horloge `monotone` (C-4) ;
    `debut`, `fin` sur l'horloge murale. Statut : reponse, delai, forme (requête impossible ou réponse retenue mal
    formée) ou reseau (envoi refusé)."""
    r = {"statut": "delai", "rcode": None, "tc": None, "reponses": None, "debut": horloge()}
    fin = monotone() + delai
    try:
        q = requete(secrets.randbelow(1 << 16) if ident is None else ident, nom, qtype, recursion)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(q, (adresse, port))
            while (reste := fin - monotone()) > 0:
                s.settimeout(reste / S)
                m, source = s.recvfrom(65535)
                if source == (adresse, port) and m[:2] == q[:2]:
                    r.update(statut="reponse", **analyser(m, q))
                    break
    except TimeoutError:
        pass
    except ValueError:                                              # Forme comprise
        r["statut"] = "forme"
    except OSError:
        r["statut"] = "reseau"
    return {**r, "fin": horloge()}
