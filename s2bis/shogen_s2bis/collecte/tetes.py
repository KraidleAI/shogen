"""Têtes de chaîne et jeton RFC 3161 quotidien (CB-15 ; E-C-35, E-C-36 ; ADR-0029 §2.8 l.218, §2.9 l.240 ; AVIS du G0,
Q-D-03 : chaque observateur horodate chaque jour sa propre tête, et celles des autres quand elles sont lisibles).
CB-15a : requête d'horodatage (TimeStampReq, RFC 3161 §2.4.1) en DER, construite en bibliothèque standard : version 1,
empreinte SHA-256 (algorithme avec paramètres NULL, octets d'OpenSSL 3.0.13), nonce s'il est donné, certificat de la TSA
demandé (certReq), ni politique ni extension ; statut d'une réponse (TimeStampResp, §2.4.2) ; manifeste des têtes, ligne
JSON canonique du journal (FORMAT §1.2), dont le sha256 est l'empreinte horodatée."""
from shogen_s2bis.collecte import journal

SHA256 = bytes.fromhex("0609608648016503040201")          # OBJECT IDENTIFIER 2.16.840.1.101.3.4.2.1 (sha256)
SEQUENCE, INTEGER, BOOLEEN, OCTETS, NUL = 0x30, 0x02, 0x01, 0x04, 0x05


class RefusJeton(ValueError):
    """Refus nommé (`code`) : JETON/empreinte, JETON/nonce, JETON/reponse."""
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


def _der(etiquette, contenu):
    """Élément DER : étiquette, longueur en forme courte sous 128 octets, longue au-delà (octets minimaux)."""
    n = len(contenu)
    longueur = bytes([n]) if n < 128 else bytes([0x80 | (k := (n.bit_length() + 7) // 8)]) + n.to_bytes(k, "big")
    return bytes([etiquette, *longueur]) + contenu


def _entier(n):
    """INTEGER DER d'un entier positif ou nul : complément à deux, octets minimaux (un zéro de tête si le bit fort)."""
    return _der(INTEGER, n.to_bytes(n.bit_length() // 8 + 1, "big"))


def requete(empreinte, nonce=None):
    """Octets DER de la requête pour `empreinte` (sha256, 32 octets) ; `nonce` : entier de 0 à 2^64 − 1, ou None."""
    if type(empreinte) is not bytes or len(empreinte) != 32:
        raise RefusJeton("JETON/empreinte", repr(empreinte)[:80])
    if nonce is not None and (type(nonce) is not int or not 0 <= nonce < 1 << 64):
        raise RefusJeton("JETON/nonce", repr(nonce)[:80])
    imprint = _der(SEQUENCE, _der(SEQUENCE, SHA256 + _der(NUL, b"")) + _der(OCTETS, empreinte))
    return _der(SEQUENCE, _entier(1) + imprint + (b"" if nonce is None else _entier(nonce)) + _der(BOOLEEN, b"\xff"))


def _element(octets, i, fin):
    """(étiquette, début du contenu, fin) de l'élément DER en `i`, qui doit finir avant `fin` ; longueur en forme
    longue de 1 à 4 octets, minimale (au moins 128, sans zéro de tête) ; sinon JETON/reponse."""
    if i + 2 > fin:
        raise RefusJeton("JETON/reponse", f"élément tronqué en {i}")
    etiquette, n, j = octets[i], octets[i + 1], i + 2
    if n & 0x80:
        k, j = n & 0x7F, j + (n & 0x7F)
        n = int.from_bytes(octets[i + 2:j], "big")
        if not 1 <= k <= 4 or j > fin or octets[i + 2] == 0 or n < 128:
            raise RefusJeton("JETON/reponse", f"longueur illisible en {i}")
    if j + n > fin:
        raise RefusJeton("JETON/reponse", f"élément en {i} au-delà de la réponse")
    return etiquette, j, j + n


def statut(tsr):
    """PKIStatus (0 accordé, 1 accordé avec modifications, 2 rejet, 3 attente, 4 et 5 révocation) d'une réponse : une
    SEQUENCE qui couvre les octets, dont le premier élément, une SEQUENCE, commence par un INTEGER d'un octet ; le
    jeton, une SEQUENCE qui finit la réponse, est présent si et seulement si le statut vaut 0 ou 1 (§2.4.2)."""
    etiquette, debut, fin = _element(tsr, 0, len(tsr))
    if etiquette != SEQUENCE or fin != len(tsr):
        raise RefusJeton("JETON/reponse", "réponse hors SEQUENCE ou octets en trop")
    etiquette, d, f = _element(tsr, debut, fin)
    if etiquette != SEQUENCE:
        raise RefusJeton("JETON/reponse", "PKIStatusInfo hors SEQUENCE")
    etiquette, ds, fs = _element(tsr, d, f)
    s = tsr[ds] if etiquette == INTEGER and fs - ds == 1 else -1
    if s not in range(6) or (f < fin) != (s in (0, 1)) or f < fin and _element(tsr, f, fin)[::2] != (SEQUENCE, fin):
        raise RefusJeton("JETON/reponse", f"statut {s}, jeton {'présent' if f < fin else 'absent'}")
    return s


def manifeste(jour, observateur, tetes):
    """Octets du manifeste du jour `jour` de `observateur` : {jour, observateur, tetes}, têtes triées par observateur
    puis journal, en ligne canonique du journal (refus JOURNAL/… d'une valeur hors JSON exact)."""
    rangees = sorted(tetes, key=lambda t: (t["observateur"], t["journal"]))
    return journal.canonique({"jour": jour, "observateur": observateur, "tetes": rangees})
