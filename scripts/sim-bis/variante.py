"""Variante non enroulée de la rotation (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lot SB-9 ; E-S-33 ; Q-S-09 (a)
de la PROPOSITION, adoptée par l'AVIS ; ADR-0029 l.141, l.143, l.205) : forme approchée de Harris (décalages de −N à N,
segment central, aucun enroulement), à décalages indépendants par unité (correction « minus » de Mrkvička et al.), sur
la suite comprimée de la strate. SB-9a : N, segment central, décalages SHA-256, série décalée sans enroulement.
regle.py n'est pas modifié : la variante en emprunte les contrôles des entrées (regle._cle). Séries : entiers, bit t =
position t de la suite comprimée. Entiers seuls : aucun flottant, aucune puissance."""
import hashlib

import commun
import regle

ETIQUETTE = "minus"                     # E-S-33 : chaîne hachée « <graine>:<strate>:minus:<r>:<u> »


def demi(n: int, diviseur, prm: dict) -> int:
    """N = ⌊n/diviseur⌋ (E-S-33 ; Q-S-09 (a) : N = ⌊n/4⌋, sensibilité N = ⌊n/8⌋) ; diviseur pris dans la section
    « variante » de parametres.json (diviseur ou sensibilite), sinon VARIANTE/diviseur."""
    v = prm["variante"]
    if type(diviseur) is not int or diviseur not in (v["diviseur"], v["sensibilite"]):
        raise commun.Refus("VARIANTE/diviseur", f"{diviseur!r} : {v['diviseur']} ou {v['sensibilite']} attendu")
    return n // diviseur


def segment(n: int, N: int) -> int:
    """Masque du segment central [N, n − N) de la suite comprimée de longueur n."""
    return ((1 << (n - N)) - 1) & ~((1 << N) - 1)


def decalage(graine: str, strate: str, r: int, u: str, N: int) -> int:
    """s(r, u) (E-S-33) : (entier big-endian des 32 octets de SHA-256 de la chaîne ASCII
    « <graine>:<strate>:minus:<r>:<u> ») modulo 2N + 1, moins N : un décalage de {−N, …, N}. Graine, strate et unité
    contrôlées par regle._cle (refus nommés de la rotation enroulée) ; r de 1 à 9 999, sinon REGLE/entier."""
    regle._cle(graine, strate, 2 * N + 1, [u])
    if type(r) is not int or not 1 <= r <= regle.R_MAX:
        raise commun.Refus("REGLE/entier", f"r = {r!r} : entier de 1 à {regle.R_MAX} attendu")
    chaine = regle.SEP.join([graine, strate, ETIQUETTE, str(r), u])
    return int.from_bytes(hashlib.sha256(chaine.encode("ascii")).digest(), "big") % (2 * N + 1) - N


def decaler(x: int, s: int, n: int, N: int) -> int:
    """Série décalée de s, sans enroulement, vue sur le segment central : la valeur de la position t va en t + s (sens
    de la rotation enroulée, Q-R-02) ; |s| ≤ N, donc chaque position du segment reçoit une position de [0, n)."""
    return (x << s if s >= 0 else x >> -s) & segment(n, N)
