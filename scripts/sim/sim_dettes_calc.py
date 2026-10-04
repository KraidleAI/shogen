"""Lot DETTES-SIM (2026-10-04) : générateurs synthétiques étendus et statistiques d'une réplication, pour
SHOGEN-SIM-NIVEAU-MODELES-1 (a : trous ; b : hétérogénéité ; c : queue lourde) et SHOGEN-FLUX-QUASI-MORT-2 /
SHOGEN-FLUX-FAIBLE-1 (alternative à choc commun sur une paire, profils de flux faibles). Paramètres : pré-enregistrement
du lot (journal G1 docs/G1-lot-DETTES-SIM.md). Répliques de r1 à f5b8269 reprises de sim_niveau_calc (poisson_binomial,
gate_value, z_score, constantes) ; N = ℓn²σ̂²_bloc en comptes entiers par lag sur masques de bits, paires (t, t + k)
toutes deux présentes (une fenêtre absente ne forme pas de paire, pt 3) ; valeur de la règle (pt 5).
Worker G1 DETTES-SIM, claude-opus-5-5."""
import bisect, hashlib, random
from decimal import Decimal, localcontext
from itertools import accumulate

import sim_niveau as S
import sim_niveau_calc as C

GRAINE, ELL, ALPHA, TROU = C.GRAINE, C.ELL, 1.5, (0.1, 60)          # trous : fraction absente, durée moyenne
LOURD = {5: (2.22263, 5.000001674588), 20: (9.7436, 20.000009008174), 60: (29.7479, 59.999999471672)}  # d0, E[D]
HETERO, MELE = (0.01,) * 6 + (0.04,) * 5, tuple((1, 5, 20, 60)[i % 4] for i in range(11))
V, _EQ = S.VALEURS, {}


def rng(chaine):
    """random.Random semé par les 8 premiers octets, big-endian, du sha256 de la chaîne ASCII (discipline de SIM-NIVEAU)."""
    return random.Random(int.from_bytes(hashlib.sha256(chaine.encode("ascii")).digest()[:8], "big")).random


def markov(p, L, n, rnd):
    """Un flux, chaîne de SIM-NIVEAU (G0 §2, §4) : n tirages ; D_1 = [U < p], puis [U < a] si D_(t−1) = 1, [U < b] sinon."""
    a, b = C.chaine(p, L)
    d = bytearray(n)
    s = d[0] = rnd() < p
    for t in range(1, n):
        s = rnd() < (a if s else b)
        if s:
            d[t] = 1
    return d


def lourd(p, L, n, rnd):
    """Un flux à durées d'écart de Lomax discrète, P(D ≥ j) = (d0/(d0 + j − 1))^1,5 (D = 1 + ⌊d0·((1 − U)^(−1/1,5) − 1)⌋),
    hors écart géométrique (début d'écart avec probabilité b = p/(E[D](1 − p)) dans une fenêtre qui suit une fenêtre
    hors écart) ; départ stationnaire : écart avec probabilité p, durée résiduelle P(R = j) = P(D ≥ j)/E[D] (j ≤ n)."""
    d0, ed = LOURD[L]
    if (L, n) not in _EQ:
        _EQ[L, n] = list(accumulate((d0 / (d0 + j)) ** ALPHA / ed for j in range(n)))
    b, d, reste = p / (ed * (1 - p)), bytearray(n), 0
    if rnd() < p:
        reste = bisect.bisect_right(_EQ[L, n], rnd()) + 1
    for t in range(n):
        if reste:
            d[t], reste = 1, reste - 1
        elif t and not d[t - 1] and rnd() < b:
            d[t], reste = 1, int(d0 * ((1.0 - rnd()) ** (-1 / ALPHA) - 1))
    return d


def presence(T, rnd):
    """Chaîne de présence, indépendante des écarts : absente au départ avec probabilité f ; P(abs → abs) = 1 − 1/G,
    P(prés → abs) = f/(G(1 − f)) ; T tirages. Rend 1 = fenêtre présente."""
    f, G = TROU
    pres, absente = bytearray(T), rnd() < f
    for t in range(T):
        if t:
            absente = rnd() < ((1 - 1 / G) if absente else f / (G * (1 - f)))
        if not absente:
            pres[t] = 1
    return pres


def serie_modele(cas, r):
    """Réplication r d'un cas de MODELES-1 : (flux, présence ou None) ; flux i = 1..11, puis la présence (cas a)."""
    ext, L, taille = cas
    rnd = rng(f"SHOGEN-DETTES-SIM-MODELES|{GRAINE}|{ext}|L={L}|{taille}|r={r}")
    if ext == "a":
        return [markov(0.02, L, taille, rnd) for _ in range(11)], presence(taille, rnd)
    if ext == "b":
        Ls = MELE if L == "mele" else (int(L),) * 11
        return [markov(p, Li, taille, rnd) for p, Li in zip(HETERO, Ls)], None
    return [lourd(0.02, L, taille, rnd) for _ in range(11)], None


def base_flux(n, r):
    """FLUX : tirages communs à tous les profils (nombres aléatoires communs) : 11 × n uniformes, puis n pour le choc."""
    rnd = rng(f"SHOGEN-DETTES-SIM-FLUX|{GRAINE}|n={n}|r={r}")
    return [[rnd() for _ in range(n)] for _ in range(12)]


def profil(U, ps, q, cache=None):
    """Flux d'un profil : D_i,t = [U_i,t < p_i] ; alternative (q > 0) : flux 1 et 2 = [U < p′] ∨ [V_t < q], p′ = (p − q)/(1 − q).
    cache : octets seuillés par (flux, seuil), partagés par les profils d'une même réplication (mêmes octets sans lui)."""
    c = {} if cache is None else cache

    def seuil(i, p):
        if (i, p) not in c:
            c[i, p] = bytes(map(float(p).__gt__, U[i]))
        return c[i, p]
    fl = [seuil(i, p) for i, p in enumerate(ps)]
    if q:
        pp, s = (ps[0] - q) / (1 - q), int.from_bytes(seuil(11, q), "little")
        for i in (0, 1):
            fl[i] = (int.from_bytes(seuil(i, pp), "little") | s).to_bytes(len(U[i]), "little")
    return fl


def valeur(tenue, z, zb):
    """Valeur de la règle (pt 5), mêmes libellés que sim_niveau.VALEURS."""
    if not tenue:
        return V[3]
    if z < C.SEUIL_Z:
        return V[1]
    return V[4] if zb is None else V[0] if zb >= C.SEUIL_Z else V[2]


def stats(flux, pres):
    """Statistiques d'une réplication (flux : octets 0/1 de longueur T ; pres : octets 0/1, None = grille complète)."""
    T = len(flux[0])
    bits = lambda o: int(o.translate(C.BITS)[::-1], 2)
    I = sum(int.from_bytes(d, "little") for d in flux).to_bytes(T, "little").translate(C.TAB)
    Pm = (1 << T) - 1 if pres is None else bits(pres)
    X = bits(I) & Pm
    n, K, e = Pm.bit_count(), X.bit_count(), [(bits(d) & Pm).bit_count() for d in flux]
    with localcontext() as ctx:
        ctx.prec = C.PREC
        phats = [+(Decimal(x) / Decimal(n)) for x in e]
    pm = C.poisson_binomial(phats)[2]
    gate = C.gate_value(n, pm)
    tenue = not gate < C.SEUIL_HIST
    z = C.z_score(n, K, pm) if tenue else None
    N = 0
    for k in range(ELL):
        Pk, Xk = Pm >> k, X >> k
        N += (ELL if k == 0 else 2 * (ELL - k)) * (n * n * (X & Xk).bit_count() + (Pm & Pk).bit_count() * K * K
                                                   - n * K * ((X & Pk).bit_count() + (Pm & Xk).bit_count()))
    with localcontext() as ctx:
        ctx.prec = C.PREC
        x = +(Decimal(K) - Decimal(n) * pm)
        zb = +(x / (Decimal(N) / Decimal(ELL * n * n)).sqrt()) if N > 0 and n >= C.N_MIN_BLOCS else None
    Ip = I if pres is None else bytes(map(int.__and__, I, pres))       # run de I : une fenêtre absente le coupe
    return {"n": n, "K": K, "e": e, "P_more": pm, "tenue": tenue, "z": z, "N": N, "z_bloc": zb, "x": x,
            "valeur": valeur(tenue, z, zb), "rmax": max(map(len, Ip.split(b"\x00"))),
            "e_grille": [d.count(1) for d in flux], "runs": [d.count(b"\x00\x01") + d[0] for d in flux]}


def compter(c, d):
    """Comptes d'une réplication dans le Counter c, mêmes clés que sim_niveau.COMPTES (et « R »)."""
    c["R"] += 1
    c[d["valeur"]] += 1
    c["garde non tenue"] += not d["tenue"]
    c["σ̂² = 0"] += d["N"] == 0
    c["z_bloc non publiée"] += d["z_bloc"] is None
    c["run maximal de I ≥ ℓ"] += d["rmax"] >= ELL
    for cle, z in (("z", d["z"]), ("z_bloc", d["z_bloc"])):
        if z is not None:
            c[cle + " ≥ 2,33"] += z >= C.SEUIL_Z
            c[cle + " ≤ −2,33"] += z <= -C.SEUIL_Z


def publique(r, d):
    """Enregistrement d'une réplication tel que publié pour l'oracle (controle_premieres) et ligne de l'empreinte."""
    s = lambda v: None if v is None else str(v)
    rec = {"r": r, "n": d["n"], "K": d["K"], "e": d["e"], "N": d["N"], "P_more": str(d["P_more"]), "z": s(d["z"]),
           "z_bloc": s(d["z_bloc"]), "valeur": d["valeur"]}
    return rec, f"{r}|{d['n']}|{d['K']}|{d['e']}|{d['N']}|{d['P_more']}|{d['z']}|{d['z_bloc']}|{d['valeur']}|{d['rmax']}\n"
