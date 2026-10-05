"""Règle SHOGEN-CRITERE-R1-2 répliquée (G0 docs/adr-0029/g0-sim/G0-SIM-BIS.md ; sous-lots SB-7 et SB-8 ; ADR-0029 §2.7
pts 2 à 6 ; E-S-24 à E-S-35) : la simulation ne l'importe pas de RECALC-BIS (Q-S-02 : réplique, recoupée par oracle
croisé à SB-13). Séries consolidées comprimées en entiers (bit t = position t de la suite comprimée des fenêtres
retenues de la strate, calendrier.comprimer). SB-7a : décalages SHA-256 (Q-R-02 adjugée), rotation enroulée, K par le
compteur « au moins deux » et S = Σ_j C(m_j, 2) par plans de bits (E-S-26). SB-7b : seuil entier, retraits D1-bis et
flux presque mort (E-S-24), unité non décalée, décision par strate avec arrêt anticipé exact et garde d'information
(E-S-28, E-S-29). Entiers et rationnels seuls : aucun flottant, aucune puissance."""
import hashlib
from fractions import Fraction

import calendrier
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


CAUSES = ("unites", "k_crit", "runs", "n_prime")


def seuil(R: int, alpha) -> int:
    """Seuil entier de C (ADR-0029 l.202) : C ≤ seuil ⇔ (C + 1)/(R + 1) ≤ α, soit seuil = α·(R + 1) − 1 (99 à R = 9 999,
    9 à R = 999 : AVIS Q-S-06), entier ≥ 0 exigé, sinon REGLE/seuil."""
    s = Fraction(*alpha) * (R + 1) - 1 if type(R) is int and R >= 1 else Fraction(-1)
    if s.denominator != 1 or s < 0:
        raise commun.Refus("REGLE/seuil", f"R = {R!r}, α = {alpha!r} : α·(R + 1) − 1 entier ≥ 0 attendu")
    return int(s)


def retraits(ok: dict, n: dict) -> dict:
    """Retraits d'une classe avant K (E-S-24 ; ADR-0029 l.170 : règle D1 reprise, flux presque mort ex ante) : ok =
    {(u, s) : fenêtres retenues de la strate s à « ok » consolidé}, n = {s : n_s, ou n′_s} ; rend {(u, s) : motif} :
    « D1-bis (a) » si u n'a aucun ok dans aucune strate (retirée partout), « D1-bis (b) » s'il n'en a aucun dans s,
    « presque mort » si 2·ok(u, s) < n(s) ; les autres unités restent."""
    out = {}
    for u in sorted({u for u, _s in ok}):
        strates = [s for s in n if (u, s) in ok]
        aucun = all(ok[u, s] == 0 for s in strates)
        for s in strates:
            if aucun:
                out[u, s] = "D1-bis (a)"
            elif ok[u, s] == 0:
                out[u, s] = "D1-bis (b)"
            elif 2 * ok[u, s] < n[s]:
                out[u, s] = "presque mort"
    return out


def premiere(btc: list):
    """Unité non décalée (ADR-0029 l.200) : premier hôte, par ordre alphabétique, du pool BTC D1-bis de la strate
    (unités BTC restées après retraits) ; None si ce pool est vide."""
    return min(btc) if btc else None


def decider(K: int, runs: int, unites: int, suffisant: bool, ks, R: int, prm: dict, S=None) -> dict:
    """Valeur de R1-2 dans une strate (E-S-28, E-S-29 ; ADR-0029 l.200-203). Entrées : K = K_s, runs de I sur la suite
    comprimée, nombre d'unités avec au moins un écart consolidé, n′_s ≥ n_s/2, itérable des (K^(r), S^(r)) pour
    r = 1, 2, … (S^(r) lu si S, valeur observée, est donnée), R. C = #{r : K^(r) ≥ K}, C1 = #{r : K^(r) ≥ k_crit − 1}
    (K_crit,s ≥ k_crit ⇔ C1 > seuil), C_S = #{r : S^(r) ≥ S} ; arrêt anticipé exact dès que C > seuil et C1 > seuil (et
    C_S > seuil si S est suivie) : les compteurs ne décroissent pas en r. Garde (causes de NON ÉVALUABLE, non
    exclusives) : unites, k_crit, runs, n_prime. REJETTE ⇔ aucune cause et C ≤ seuil. Moins de R rotations sans arrêt :
    REGLE/rotations."""
    g, s_, it = prm["regle"]["garde"], seuil(R, prm["regle"]["alpha"]), iter(ks)
    c = c1 = cs = 0
    for r in range(1, R + 1):
        try:
            k, sr = next(it)
        except StopIteration:
            raise commun.Refus("REGLE/rotations", f"{r - 1} rotations, R = {R}") from None
        c, c1 = c + (k >= K), c1 + (k >= g["k_crit"] - 1)
        if S is not None:
            cs += sr >= S
        if c > s_ and c1 > s_ and (S is None or cs > s_):
            break
    causes = [x for x, v in zip(CAUSES, (unites < g["unites"], c1 <= s_, runs < g["runs"], not suffisant)) if v]
    valeur = "NON ÉVALUABLE" if causes else "REJETTE" if c <= s_ else "NE REJETTE PAS"
    return {"valeur": valeur, "causes": causes, "C": c, "C1": c1, "C_S": None if S is None else cs, "r": r}


def rotation(series: dict, premier, graine: str, strate: str, r: int, n: int) -> list:
    """Séries tournées de la rotation r (rotations jointes par hôte : o(r, u) ne dépend pas de la classe, ADR-0029
    l.200) ; l'unité `premier` n'est pas décalée (None : toutes le sont)."""
    return [x if u == premier else tourner(x, decalage(graine, strate, r, u, n), n) for u, x in series.items()]


def tester(series: dict, premier, graine: str, strate: str, n: int, n_s: int, prm: dict, R: int, avec_S=False) -> dict:
    """R1-2 pour une classe dans une strate : series = {u : D(u, ·) comprimée sur les n fenêtres retenues (n_s, ou
    n′_s)} des unités restées après retraits ; premier : unité non décalée (premiere) ; graine de règle de la
    réplication (aleas.graine_regle) ; strate parmi calibration.strates (sinon REGLE/libelle) ; rend decider(), plus K,
    S, runs et unites. Avec au plus une série non nulle, K^(r) = S^(r) = 0 pour tout r, exactement : aucune rotation
    calculée."""
    if strate not in prm["calibration"]["strates"]:
        raise commun.Refus("REGLE/libelle", f"strate {strate!r}")
    vals = list(series.values())
    i, unites, S = deux(vals), sum(1 for x in vals if x), paires(vals) if avec_S else None

    def ks():
        for r in range(1, R + 1):
            rot = rotation(series, premier, graine, strate, r, n) if unites >= 2 else []
            yield deux(rot).bit_count(), paires(rot) if avec_S else None
    out = decider(i.bit_count(), calendrier.runs(i), unites, 2 * n >= n_s, ks(), R, prm, S)
    out.update(K=i.bit_count(), S=S, runs=calendrier.runs(i), unites=unites)
    return out
