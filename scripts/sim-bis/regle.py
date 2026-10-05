"""Règle SHOGEN-CRITERE-R1-2 répliquée (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lots SB-7 et SB-8 ; ADR-0029 §2.7
pts 2 à 6 ; E-S-24 à E-S-35) : la simulation ne l'importe pas de RECALC-BIS (Q-S-02 : réplique, recoupée par oracle
croisé à SB-13). Séries consolidées comprimées en entiers (bit t = position t de la suite comprimée des fenêtres
retenues de la strate, calendrier.comprimer). SB-7a : décalages SHA-256 (Q-R-02 adjugée), rotation enroulée, K par le
compteur « au moins deux » et S = Σ_j C(m_j, 2) par plans de bits (E-S-26). Entiers seuls : aucun flottant, aucune
puissance."""
import hashlib

import commun

SEP = ":"


def _libelle(v, nom: str) -> str:
    if type(v) is str and v != "" and all(" " <= ch <= "~" for ch in v) and SEP not in v:
        return v
    raise commun.Refus("REGLE/libelle", f"{nom} = {v!r} : ASCII imprimable, sans « {SEP} »")


def decalage(graine: str, strate: str, r: int, u: str, n: int) -> int:
    """o(r, u) (E-S-27 ; ADR-0029 l.200 ; Q-R-02 adjugée, AVIS-C l.57-63) : entier big-endian des 32 octets de SHA-256
    de la chaîne ASCII « <graine>:<strate>:<r>:<u> », modulo n (n_s, ou n′_s, de la strate). Graine : 64 hexadécimaux
    minuscules (sinon REGLE/graine) ; strate et unité en ASCII imprimable, sans « : » (sinon REGLE/libelle) ; r ≥ 1,
    en décimal sans zéro de tête, et n ≥ 1 entiers (sinon REGLE/entier)."""
    if not commun.hex64(graine):
        raise commun.Refus("REGLE/graine", f"{graine!r} : 64 hexadécimaux minuscules attendus")
    if type(r) is not int or r < 1 or type(n) is not int or n < 1:
        raise commun.Refus("REGLE/entier", f"r = {r!r}, n = {n!r} : entiers ≥ 1 attendus")
    chaine = SEP.join([graine, _libelle(strate, "strate"), str(r), _libelle(u, "unité")])
    return int.from_bytes(hashlib.sha256(chaine.encode("ascii")).digest(), "big") % n


def tourner(x: int, o: int, n: int) -> int:
    """Rotation enroulée de la suite comprimée de longueur n (ADR-0029 l.200 ; sens de Q-R-02) : la valeur de la
    position t va en (t + o) mod n, 0 ≤ o < n."""
    return ((x << o) | (x >> (n - o))) & ((1 << n) - 1)


def deux(series: list) -> int:
    """Masque I des positions où au moins deux séries valent 1 (compteur « au moins deux » sur masques de bits,
    E-S-26) : K = |I| (ADR-0029 §2.4 : K_s = #{j : m_j ≥ 2}) ; les runs de I se comptent sur la suite comprimée
    (E-S-28)."""
    un = au_moins_deux = 0
    for x in series:
        au_moins_deux |= un & x
        un |= x
    return au_moins_deux


def paires(series: list) -> int:
    """S = Σ_j C(m_j, 2) (E-S-26 ; ADR-0029 l.164, l.212) : m_j en quatre plans de bits p_b (additionneur à retenue, au
    plus 15 séries, sinon REGLE/plans), puis S = Σ_b ((4^b − 2^b)/2)·|p_b| + Σ_{b<c} 2^(b+c)·|p_b ∧ p_c|, puisque
    m² = Σ_b 4^b·p_b + 2·Σ_{b<c} 2^(b+c)·p_b·p_c ; puissances de deux par décalage."""
    if len(series) > 15:
        raise commun.Refus("REGLE/plans", f"{len(series)} séries : au plus 15")
    p = [0, 0, 0, 0]
    for x in series:
        for b in range(4):
            p[b], x = p[b] ^ x, p[b] & x
    s = 0
    for b in range(4):
        s += (((1 << (2 * b)) - (1 << b)) >> 1) * p[b].bit_count()
        for c in range(b + 1, 4):
            s += (1 << (b + c)) * (p[b] & p[c]).bit_count()
    return s
