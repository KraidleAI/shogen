"""Loi de rotation de la règle R1-2 (RB-6 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION E-R-16 à E-R-18, AVIS Q-R-02 ;
ADR-0029 §2.4 c, §2.7 pts 2, 4 et 9). Contrat d'entrée et de sortie, oracle croisé de SIM-BIS (SB-13, E-S-51) :
docs/adr-0029/s2bis/ROTATION-S2BIS.md. Position t = 0 … n − 1 : rang dans la suite comprimée (ordre chronologique) ;
série d'une unité : entier-masque, bit t = D(u, t), 0 <= masque < 2**n. o(r, u) = entier big-endian des 32 octets de
SHA-256 des octets UTF-8 de « <graine>:<strate>:<r>:<u> », modulo n (n_s, n′_s ou longueur de la sous-suite), jamais
de la classe : rotations jointes par hôte. La valeur de la position t va en (t + o) mod n. Tout écart d'entrée lève
RefusRotation (code nommé), avant tout calcul."""
import hashlib
import re

STRATES = ("calme", "stress")                             # libellés scellés (AVIS Q-R-02, complément (1))
GRAINE = re.compile("[0-9a-f]{64}")                        # sha256 du manifeste, forme imprimée au README du sceau


class RefusRotation(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} : {detail}")
        self.code = code


def _exiger(ok, code, detail):
    if not ok:
        raise RefusRotation(code, detail)


def _entier(v, bas, haut=None):
    return type(v) is int and v >= bas and (haut is None or v <= haut)


def _unite(u):
    """Nom d'hôte de configuration : ASCII imprimable, sans « : » (séparateur de l'entrée de SHA-256)."""
    return type(u) is str and u != "" and ":" not in u and all(" " <= c <= "~" for c in u)


def _entrees(graine, strate, n):
    _exiger(type(graine) is str and GRAINE.fullmatch(graine), "ROTATION/graine", repr(graine))
    _exiger(type(strate) is str and strate in STRATES, "ROTATION/strate", repr(strate))
    _exiger(_entier(n, 1), "ROTATION/n", repr(n))


def _o(graine, strate, r, u, n):
    return int.from_bytes(hashlib.sha256(f"{graine}:{strate}:{r}:{u}".encode("utf-8")).digest(), "big") % n


def decalage(graine, strate, r, u, n):
    """o(r, u) ; r de 1 à 9 999, écrit en décimal sans zéro de tête (AVIS Q-R-02, complément (2))."""
    _entrees(graine, strate, n)
    _exiger(_entier(r, 1, 9999), "ROTATION/r", repr(r))
    _exiger(_unite(u), "ROTATION/unite", repr(u))
    return _o(graine, strate, r, u, n)


def tourner(m, o, n):
    """Masque `m` de n bits décalé de o positions (0 <= o < n) : le bit t va en (t + o) mod n."""
    return ((m << o) | (m >> (n - o))) & ((1 << n) - 1)
