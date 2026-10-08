"""Loi de rotation de la règle R1-2 (RB-6 ; G0 docs/adr-0029/g0-collecte/, PROPOSITION E-R-16 à E-R-18, AVIS Q-R-02 ;
ADR-0029 §2.4 c, §2.7 pts 2, 4 et 9). Contrat d'entrée et de sortie, oracle croisé de SIM-BIS (SB-13, E-S-51) :
docs/adr-0029/s2bis/ROTATION-S2BIS.md. Position t = 0 … n − 1 : rang dans la suite comprimée (ordre chronologique) ;
série d'une unité : entier-masque, bit t = D(u, t), 0 <= masque < 2**n. o(r, u) = entier big-endian des 32 octets de
SHA-256 des octets UTF-8 de « <graine>:<strate>:<r>:<u> », modulo n (n_s, n′_s ou longueur de la sous-suite), jamais
de la classe : rotations jointes par hôte. La valeur de la position t va en (t + o) mod n. Tout écart d'entrée lève
RefusRotation (code nommé), avant tout calcul."""
import hashlib
import re
from fractions import Fraction

STRATES = ("calme", "stress")                             # libellés scellés (AVIS Q-R-02, complément (1))
GRAINE = re.compile("[0-9a-f]{64}")                        # sha256 du manifeste, forme imprimée au README du sceau
# Unité : nom d'hôte de configuration (E-R-15) en minuscules, lettres a à z, chiffres, « - » et « . », de 1 à 253
# caractères (Q-RB-13 de la G2 de RB-T1, resserrement du complément (3) de l'AVIS Q-R-02 : ni « : », séparateur de
# l'entrée de SHA-256, ni espace, ni majuscule) ; la même règle au chargeur (`config_analyse._nom`).
HOTE = re.compile("[a-z0-9.-]{1,253}")


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
    """Nom d'hôte de configuration, règle HOTE."""
    return type(u) is str and HOTE.fullmatch(u) is not None


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


def compter(masques):
    """(K, S) : K = #{t : m_t >= 2}, S = Σ_t C(m_t, 2) = Σ des paires u < v de #(D_u ∧ D_v), m_t = Σ_u D(u, t)."""
    un = deux = s = 0
    vus = []
    for m in masques:
        deux |= un & m
        un |= m
        s += sum((m & v).bit_count() for v in vus)
        vus.append(m)
    return deux.bit_count(), s


def resume(x, loi, seuil):
    """(C, x_crit, moyenne) : C = #{r : x^(r) >= x} ; x_crit = plus petit k >= 0 tel que #{r : x^(r) >= k} <= seuil,
    soit la valeur de rang seuil + 1 de la loi triée en ordre décroissant, plus un ; moyenne exacte (Fraction)."""
    tri = sorted(loi, reverse=True)
    return sum(v >= x for v in loi), tri[seuil] + 1 if seuil < len(tri) else 0, Fraction(sum(loi), len(loi))


def lois(graine, strate, n, classes, premiere, R, seuil):
    """Lois de K et de S sous R rotations (r = 1 … R), rotations jointes par hôte : o(r, u) commun à toutes les classes.
    `classes` : {classe: {unité: masque}} ; `premiere` : unité jamais décalée (premier hôte du pool BTC D1-bis de la
    strate, ADR-0029 l.200), ou None ; absente d'une classe, toutes les unités de la classe sont décalées. R de 1 à
    9 999 et seuil (99 pour R = 9 999) : bloc `rotations` de analyse.json. Rend {classe: {"K", "C", "K_crit",
    "K_moyen", "K_r", "S", "C_S", "S_crit", "S_moyen", "S_r"}}, classes triées ; K_r[r - 1] = K^(r)."""
    _entrees(graine, strate, n)
    _exiger(_entier(R, 1, 9999) and _entier(seuil, 0), "ROTATION/R", f"R = {R!r}, seuil = {seuil!r}")
    _exiger(type(classes) is dict and all(type(c) is str and type(s) is dict for c, s in classes.items()),
            "ROTATION/classes", type(classes).__name__)
    _exiger(premiere is None or _unite(premiere), "ROTATION/unite", repr(premiere))
    for c, series in classes.items():
        for u, m in series.items():
            _exiger(_unite(u), "ROTATION/unite", f"{c} : {u!r}")
            _exiger(_entier(m, 0) and m >> n == 0, "ROTATION/masque", f"{c} : {u} hors de [0, 2**{n})")
    tri = {c: sorted(classes[c].items()) for c in sorted(classes)}
    hotes = sorted({u for s in tri.values() for u, _m in s} - {premiere})
    K_r, S_r = {c: [] for c in tri}, {c: [] for c in tri}
    for r in range(1, R + 1):
        o = {u: _o(graine, strate, r, u, n) for u in hotes}
        for c, series in tri.items():
            k, s = compter(m if u == premiere else tourner(m, o[u], n) for u, m in series)
            K_r[c].append(k)
            S_r[c].append(s)
    sortie = {}
    for c, series in tri.items():
        K, S = compter(m for _u, m in series)
        sortie[c] = {"K": K, **dict(zip(("C", "K_crit", "K_moyen"), resume(K, K_r[c], seuil))), "K_r": K_r[c],
                     "S": S, **dict(zip(("C_S", "S_crit", "S_moyen"), resume(S, S_r[c], seuil))), "S_r": S_r[c]}
    return sortie
