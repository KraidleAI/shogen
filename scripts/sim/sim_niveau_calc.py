"""SHOGEN-SIM-NIVEAU-1, sous-lot SIM-NIVEAU-a1 : générateur et statistiques d'une réplication (G0 du lot, §2, §4, §5).
Modèle nul : 11 flux simulés, mutuellement indépendants par construction (doc 10 §5.1), chacun chaîne de Markov
stationnaire à deux états ; z (plug-in, répliques de r1 à f5b8269), σ̂²_bloc (ℓ = 240) en deux formes entières, z_bloc,
valeur de la règle SHOGEN-CRITERE-R1-1 (ADR-0028 §1 bis.1 pts 3 et 5). Spécification : G0 (sha256 4e4dcf13…f948) et
cp-1 (sha256 ece81297…6303). Bibliothèque standard seule ; `python -B`. Rédaction : worker G1 claude-opus-5-5, 2026-09-30."""
import hashlib, math, os, random
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import accumulate
from operator import sub

NSRC, ELL, PREC, GRAINE = 11, 240, 50, 20260930
SEUIL_Z, SEUIL_HIST = Decimal("2.33"), Decimal(10)            # r1.py l.58 et l.56 à f5b8269
N_MIN_BLOCS = 30 * ELL                                        # garde de blocs, §1 bis.1 pt 3
CHAINE = "SHOGEN-SIM-NIVEAU-1|{g}|p={p!r}|L={L}|n={n}|r={r}"  # C-5 : p={p!r} ; à p = 0.02, chaîne du G0 §4
TAB = bytes([0, 0] + [1] * 254)                                # m_t -> I_t = 1{m_t >= 2}
BITS = bytes.maketrans(b"\x00\x01", b"01")
_MARGES = {}                                                   # n -> (m_j des blocs, Σ m_j²)


def graine(p, L, n, r):
    """Graine de la réplication r du cas (L, n) : 8 premiers octets, big-endian, du sha256 de la chaîne (G0 §4)."""
    h = hashlib.sha256(CHAINE.format(g=GRAINE, p=p, L=L, n=n, r=r).encode("ascii")).digest()
    return int.from_bytes(h[:8], "big")


def chaine(p, L):
    """(a, b) = (P(D_t = 1 | D_t-1 = 1), P(D_t = 1 | D_t-1 = 0)) ; G0 §2 : L = 1 := tirages indépendants."""
    return (p, p) if L == 1 else (1.0 - 1.0 / L, p / (L * (1.0 - p)))


def generer(p, L, n, rng):
    """11·n appels à rng.random(), flux i = 1..11 puis t = 1..n (G0 §4) ; rend (m_t en octets, e_i, runs d'écart_i)."""
    a, b = chaine(p, L)
    rnd, somme, e, runs = rng.random, 0, [], []
    for _ in range(NSRC):
        d = bytearray(n)
        s = d[0] = rnd() < p                                   # état initial : loi stationnaire
        for t in range(1, n):
            s = rnd() < (a if s else b)
            if s:
                d[t] = 1
        e.append(d.count(1))
        runs.append(d.count(b"\x00\x01") + d[0])
        somme += int.from_bytes(d, "little")                   # chiffres en base 256 <= 11 : aucune retenue
    return somme.to_bytes(n, "little"), e, runs


def poisson_binomial(phats):
    """Réplique ligne à ligne de r1.poisson_binomial (r1.py l.199-216 à f5b8269)."""
    with localcontext() as ctx:
        ctx.prec = PREC
        one = Decimal(1)
        p0 = one
        for p in phats:
            p0 *= (one - p)
        p1 = Decimal(0)
        for i, pi in enumerate(phats):
            term = pi
            for j, pj in enumerate(phats):
                if j != i:
                    term *= (one - pj)
            p1 += term
        p_more = one - p0 - p1
        return +p0, +p1, +p_more


def gate_value(n, p_more):
    """Réplique de r1.gate_value (l.219-223)."""
    with localcontext() as ctx:
        ctx.prec = PREC
        return +(Decimal(n) * p_more * (Decimal(1) - p_more))


def z_score(n, k, p_more):
    """Réplique de r1.z_score (l.231-238)."""
    with localcontext() as ctx:
        ctx.prec = PREC
        mean = Decimal(n) * p_more
        var = Decimal(n) * p_more * (Decimal(1) - p_more)
        return +((Decimal(k) - mean) / var.sqrt())


def num_blocs(I, n, K):
    """N_bloc = n²·A − 2nK·B + K²·C = ℓn²σ̂² (identité de la CRITIQUE v2 §4.1 ; G0 §5.3) : blocs j = 1−ℓ..n−1 de
    longueur ℓ sur la série complétée par des 0 ; c_j = nombre de I = 1 du bloc j, m_j = fenêtres présentes du bloc j."""
    if n not in _MARGES:
        ms = [min(j + ELL, n) - max(j, 0) for j in range(1 - ELL, n)]
        _MARGES[n] = (ms, math.sumprod(ms, ms))
    ms, C = _MARGES[n]
    pre = [0] * ELL + list(accumulate(I)) + [K] * (ELL - 1)   # pre[v] = Σ I_t sur les min(max(v−ℓ+1, 0), n) premières
    cs = list(map(sub, pre[ELL:], pre[:-ELL]))                 # c_j, j = 1−ℓ..n−1
    return n * n * math.sumprod(cs, cs) - 2 * n * K * math.sumprod(cs, ms) + K * K * C


def num_lags(I, n, K):
    """(N_lag, n²γ̂₀) : N_lag = Σ_{k<ℓ} W_k·(n²C_k − nK(S_k + S′_k) + K²M_k), W_0 = ℓ, W_k = 2(ℓ − k) ; comptes entiers
    par lag sur masques de bits (bit t = I_t), grille complète (M_k = n − k) : forme prescrite à B-DEP-1 (pt 3)."""
    X = int(I.translate(BITS)[::-1], 2)
    tot = g0 = 0
    for k in range(ELL):
        C, S, S2 = (X & (X >> k)).bit_count(), (X & ((1 << (n - k)) - 1)).bit_count(), (X >> k).bit_count()
        g = n * n * C - n * K * (S + S2) + K * K * (n - k)       # n²·γ̂_k
        tot += (ELL if k == 0 else 2 * (ELL - k)) * g
        g0 = g if k == 0 else g0
    return tot, g0


def replication(p, L, n, r):
    """Réplication r du cas (L, n) (G0 §5) : comptes ; plug-in et z (r1) ; σ̂² en deux formes ; z_bloc ; valeur (pt 5) ;
    drapeaux des oracles (2) n²γ̂₀ des comptes du lag 0 = n·K(n − K) et (2b) N_lag = N_bloc, exigés par l'agrégation."""
    cnt, e, runs = generer(p, L, n, random.Random(graine(p, L, n, r)))
    I = cnt.translate(TAB)
    K = I.count(1)
    with localcontext() as ctx:
        ctx.prec = PREC
        phats = [+(Decimal(x) / Decimal(n)) for x in e]         # r1.compute_r1 l.450-452
    p0, p1, pm = poisson_binomial(phats)
    gate = gate_value(n, pm)
    tenue = not gate < SEUIL_HIST                               # r1.insufficient_history (l.226-228) : « < »
    z = z_score(n, K, pm) if tenue else None
    nb, (nl, g0) = num_blocs(I, n, K), num_lags(I, n, K)
    publiee = nb > 0 and n >= N_MIN_BLOCS
    with localcontext() as ctx:
        ctx.prec = PREC
        zb = +((Decimal(K) - Decimal(n) * pm) / (Decimal(nb) / Decimal(ELL * n * n)).sqrt()) if publiee else None
    if not tenue:
        v = "NON ÉVALUABLE (garde §5.4)"
    elif z < SEUIL_Z:
        v = "NE REJETTE PAS (z < 2,33)"
    elif zb is None:
        v = "NON ÉVALUABLE (rejet non qualifiable)"
    else:
        v = "REJETTE" if zb >= SEUIL_Z else "NE REJETTE PAS (discordance)"
    nr, rmax, q = I.count(b"\x00\x01") + I[0], max(map(len, I.split(b"\x00"))), Fraction(gate)
    return {"e": e, "runs": runs, "K": K, "phats": phats, "P0": p0, "P1": p1, "P_more": pm, "garde": gate,
            "tenue": tenue, "z": z, "N": nb, "z_bloc": zb, "valeur": v, "ok2": g0 == n * K * (n - K), "ok2b": nl == nb,
            "FIV": float(Fraction(nb, ELL * n * n) / q) if q else None,
            "R_centrage": float(Fraction(K * (n - K), n) / q) if q else None,
            "FIV_serie": float(Fraction(nb, ELL * n * K * (n - K))) if 0 < K < n else None, "runs_I": nr, "rmax": rmax,
            "ligne": f"{r}|{K}|{e}|{runs}|{nb}|{pm}|{gate}|{z}|{zb}|{v}|{nr}|{rmax}\n"}


def tache(args):
    """Tâche du Pool : (p, L, n, r) -> enregistrement, avec le PID qui l'a servie (C-6 ; hors sorties bit-identiques)."""
    d = replication(*args)
    d["pid"] = os.getpid()
    return d
