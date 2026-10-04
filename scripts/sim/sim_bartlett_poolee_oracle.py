"""SHOGEN-BARTLETT-BIAIS-1 et SHOGEN-POOLEE-BLOC-1 (b) (lot DETTES-SIM) : oracle de sim_bartlett_poolee.py, écrit avant
le générateur. (B0) paramètres = pré-enregistrement (p = 0,02 ; L ∈ {1, 5, 20, 60} ; n ∈ {10⁴ ; 2,5·10⁴} ; R/diviseur).
(B1) références exactes recalculées par d'autres voies que le générateur : R(k) par convolution des 11 lois de paires
     (comptes tronqués à 2), Var(K) et σ²_∞ par sommes directes, E[σ̂²_bloc] par la forme en sommes de blocs
     (1/ℓ)·Σ_j E[B_j²], E_centre_sur_P = Σ_{|k|<ℓ} (1 − |k|/ℓ)(n − |k|)R(k) et kunsch_premier_ordre = −(n/ℓ)·Σ 2k·R(k)
     (correction C-1 du G2) ; égalité à 10⁻⁹ près en relatif ; une référence nulle en théorie (Künsch à L = 1, où la
     convolution ne rend que du bruit, |x| ≤ 10⁻⁹·Var(K)) se compare à l'échelle de Var(K).
     (B2) taux recalculés depuis les comptes ; inclusions.
(B3) r < 20 de chaque L : série régénérée sans sim_niveau_calc (sim_niveau_oracle_r1.serie), N contre
     r1.block_long_run_variance, P̂_more par r1.poisson_binomial, z_pool par r1.z_pool_stratifie, forme par blocs ;
     10⁻⁴⁰ près en relatif. (B4, --complet, pour les exécutions réduites) : toutes les réplications refaites
     (sim_niveau_calc.replication) et les huit comptes de taux recomptés par un code distinct de l'agrégation du
     générateur (Decimal ; z_pool par r1.z_pool_stratifie). Sortie ≠ 0 au premier écart, aucun fichier ; sinon
     enregistrement JSON (mode xb).
Usage : python3.13 -B sim_bartlett_poolee_oracle.py --r1 EXPORT/s2-harness --commit SHA --json bartlett_poolee.json
--sortie F.json      Worker G1 DETTES-SIM, claude-opus-5-5, 2026-10-04."""
import argparse, hashlib, json, math, os, sys
from decimal import Decimal, localcontext
from fractions import Fraction

P, LS, NS, R0, ELL, NF, W = 0.02, (1, 5, 20, 60), (10000, 25000), 5000, 240, 11, 60


def echec(t, msg):
    sys.exit(f"ECHEC ({t}) : {msg}")


def rk_conv(L, kmax):
    """R(k) de I_t = 1{m_t ≥ 2}, k = 0..kmax : loi jointe de (min(m_t, 2), min(m_t+k, 2)) par convolution des 11 paires."""
    a, b = (P, P) if L == 1 else (1.0 - 1.0 / L, P / (L * (1.0 - P)))
    lam, out = a - b, []
    for k in range(kmax + 1):
        g = lam ** k if k else 1.0
        x11, x10 = P * (P + (1 - P) * g), P * (1 - P) * (1 - g)
        loi = {(1, 1): x11, (1, 0): x10, (0, 1): x10, (0, 0): 1 - x11 - 2 * x10}
        t = {(0, 0): 1.0}
        for _ in range(NF):
            u = {}
            for (i, j), v in t.items():
                for (di, dj), w in loi.items():
                    c = (min(i + di, 2), min(j + dj, 2))
                    u[c] = u.get(c, 0.0) + v * w
            t = u
        out.append(t.get((2, 2), 0.0))
    pm = 1 - (1 - P) ** NF - NF * P * (1 - P) ** (NF - 1)
    return [x - pm * pm for x in out]


def references(L, n):
    """(Var(K), n·σ²_∞, E[σ̂²_bloc], E_centre_sur_P, premier ordre de Künsch) ; R(k) nulle au-delà du k où
    |λ|^k < 10⁻²⁰ (terme négligé < 10⁻¹⁵ en relatif)."""
    lam = 0.0 if L == 1 else (1.0 - 1.0 / L) - P / (L * (1.0 - P))
    kmax = min(n - 1, max(ELL, 1 if lam == 0 else int(math.log(1e-20) / math.log(lam)) + 1))
    R = rk_conv(L, kmax) + [0.0] * (n - 1 - kmax)
    vk = math.fsum([n * R[0]] + [2 * (n - j) * R[j] for j in range(1, n)])
    s_inf = n * math.fsum([R[0]] + [2 * x for x in R[1:]])
    cum = [0.0]
    for x in R[1:]:
        cum.append(cum[-1] + x)
    A = [R[0] + cum[t - 1] + cum[n - t] for t in range(1, n + 1)]
    pa = [0.0]
    for x in A:
        pa.append(pa[-1] + x)
    vbar = pa[n] / (n * n)
    H = [0.0] + [m * R[0] + 2 * math.fsum((m - d) * R[d] for d in range(1, m)) for m in range(1, ELL + 1)]
    tot = []
    for j in range(1 - ELL, n):
        s, e = max(j, 0), min(j + ELL, n)
        m = e - s
        tot.append(H[m] - 2 * m / n * (pa[e] - pa[s]) + m * m * vbar)
    e_c = math.fsum([n * R[0]] + [2 * (1 - k / ELL) * (n - k) * R[k] for k in range(1, ELL)])
    return vk, s_inf, math.fsum(tot) / ELL, e_c, -n / ELL * math.fsum(2 * k * R[k] for k in range(1, n))


def ecart_rel(x, y):
    fx, fy = Fraction(x), Fraction(y)
    return abs(fx - fy) / abs(fx) if fx else abs(fy)


def complet(r1, J, R):
    """(B4) Recomptage de toutes les réplications : z à P connu, z_bloc à P connu, z à Var(K) exacte, z et z_bloc
    plug-in, z_pool, forme par blocs, les deux ; égalité exacte des comptes avec la sortie."""
    import sim_niveau_calc as C
    s, nb = Decimal("2.33"), 0
    for L in LS:
        cpt = {n: [0] * 5 for n in NS}
        cp = [0, 0, 0]
        vk = {n: Decimal(references(L, n)[0]) for n in NS}
        for r in range(R):
            recs = [C.replication(P, L, n, r) for n in NS]
            with localcontext(r1.contexte_decimal()):
                pd = Decimal(1) - (1 - Decimal(P)) ** NF - NF * Decimal(P) * (1 - Decimal(P)) ** (NF - 1)
                for n, d in zip(NS, recs):
                    x, s2 = Decimal(d["K"]) - n * pd, Decimal(d["N"]) / (ELL * n * n)
                    ind = (x / (n * pd * (1 - pd)).sqrt() >= s, d["N"] > 0 and x / s2.sqrt() >= s,
                           x / vk[n].sqrt() >= s, d["z"] is not None and d["z"] >= s,
                           d["z_bloc"] is not None and d["z_bloc"] >= s)
                    cpt[n] = [u + bool(v) for u, v in zip(cpt[n], ind)]
                num, _, z = r1.z_pool_stratifie([(n, d["K"], d["P_more"]) for n, d in zip(NS, recs)])
                zp = z if all(d["tenue"] for d in recs) else None
                zb = (num / sum(Decimal(d["N"]) / (ELL * n * n) for n, d in zip(NS, recs)).sqrt()
                      if all(d["N"] > 0 for d in recs) else None)
            cp = [u + bool(v) for u, v in zip(cp, (zp is not None and zp >= s, zb is not None and zb >= s,
                                                   zp is not None and zb is not None and min(zp, zb) >= s))]
            nb += 1
        for c in J["bartlett"]:
            if c["L"] == L and [c["taux"][k]["x"] for k in c["taux"]] != cpt[c["n"]]:
                echec("B4", f"comptes de taux, L={L} n={c['n']} : sortie {[c['taux'][k]['x'] for k in c['taux']]}, "
                            f"oracle {cpt[c['n']]}")
        if [J["poolee"][LS.index(L)]["taux"][k]["x"] for k in ("z_pool", "z_pool_bloc", "min")] != cp:
            echec("B4", f"comptes de la poolée, L={L} : oracle {cp}")
    return nb


def main():
    ap = argparse.ArgumentParser(description="oracle de SHOGEN-BARTLETT-BIAIS-1 et SHOGEN-POOLEE-BLOC-1 (b)")
    for nom in ("--r1", "--commit", "--json", "--sortie"):
        ap.add_argument(nom, required=True)
    ap.add_argument("--complet", action="store_true")
    a = ap.parse_args()
    if os.path.exists(a.sortie):
        sys.exit("refus : le fichier de sortie existe deja")
    sys.path[:0] = [os.path.dirname(os.path.abspath(__file__)), os.path.abspath(a.r1)]
    import sim_niveau_oracle_r1 as O
    from shogen_s2 import r1
    J = json.loads(open(a.json, "rb").read().decode("utf-8"))
    pa, dv = J["parametres"], J["parametres"]["diviseur"]
    R = R0 // dv
    if (pa["p"], pa["L"], pa["n"], pa["R"], pa["ell"]) != (repr(P), list(LS), list(NS), R, ELL):
        echec("B0", "paramètres de la sortie différents du pré-enregistrement")
    if [(c["L"], c["n"]) for c in J["bartlett"]] != [(L, n) for L in LS for n in NS] or [
            c["L"] for c in J["poolee"]] != list(LS):
        echec("B0", "cas de la sortie différents du pré-enregistrement")
    e1 = 0.0
    for c in J["bartlett"]:
        ref = references(c["L"], c["n"])
        for nom, x in zip(("var_K_exacte", "n_sigma2_inf", "E_sigma2_bloc_exacte", "E_centre_sur_P",
                           "kunsch_premier_ordre"), ref):
            d = abs(c["exact"][nom] - x) / (abs(x) if abs(x) > 1e-9 * ref[0] else ref[0])
            e1 = max(e1, d)
            if d > 1e-9:
                echec("B1", f"{nom} : sortie {c['exact'][nom]!r}, oracle {x!r}, L={c['L']} n={c['n']}")
    nb2 = 0
    for c in J["bartlett"] + J["poolee"]:
        for nom, u in c["taux"].items():
            r = u["x"] / R
            ok = (u["r"] == r and math.isclose(u["SE"], math.sqrt(r * (1 - r) / R), rel_tol=1e-12, abs_tol=0)
                  and u["borne95_si_x_nul"] == (1 - 0.05 ** (1 / R) if u["x"] == 0 else None) and 0 <= u["x"] <= R)
            if not ok:
                echec("B2", f"taux {nom}, L={c['L']}")
            nb2 += 1
    for c in J["poolee"]:
        t = c["taux"]
        if not t["min"]["x"] <= min(t["z_pool"]["x"], t["z_pool_bloc"]["x"]):
            echec("B2", f"REJETTE poolée (les deux) > min des deux, L={c['L']}")
    e3, n3 = Fraction(0), 0
    for c in J["poolee"]:
        L = c["L"]
        for r, (zp, zpb) in enumerate(c["controle_premieres"]):
            st = []
            for n in NS:
                e, _runs, I = O.serie(P, L, n, r)
                v = r1.block_long_run_variance([(W * t, i) for t, i in enumerate(I)], W)
                with localcontext(r1.contexte_decimal()):
                    ph = [+(Decimal(x) / Decimal(n)) for x in e]
                pm = r1.poisson_binomial(ph)[2]
                st.append((n, v["K"], pm, v["numerateur"], r1.insufficient_history(n, pm)))
            num, var, z = r1.z_pool_stratifie([(n, k, pm) for n, k, pm, _, _ in st])
            zr = None if any(h for *_, h in st) else z
            with localcontext(r1.contexte_decimal()):
                s2 = sum((Decimal(N) / Decimal(ELL * n * n) for n, _, _, N, _ in st), Decimal(0))
                zbr = +(num / s2.sqrt()) if all(N > 0 for *_, N, _ in st) else None
            for nom, x, y in (("z_pool", zr, zp), ("z_pool_bloc", zbr, zpb)):
                if (x is None) != (y is None) or (x is not None and ecart_rel(x, Decimal(y)) > Fraction(1, 10 ** 40)):
                    echec("B3", f"{nom} : r1 {x}, sortie {y}, L={L} r={r}")
                e3 = max(e3, ecart_rel(x, Decimal(y)) if x is not None else Fraction(0))
            n3 += 1
    n4 = complet(r1, J, R) if a.complet else 0
    b = open(r1.__file__, "rb").read()
    sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
    rec = {"oracle": "SHOGEN-BARTLETT-BIAIS-1 et SHOGEN-POOLEE-BLOC-1 (b) : pré-enregistrement, références exactes, "
                     "taux, r1", "commit_r1": a.commit, "blob_r1": hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest(),
           "sha256_r1": hashlib.sha256(b).hexdigest(), "json": {os.path.basename(a.json): sha(a.json)},
           "script_sha256": {os.path.basename(f): sha(f) for f in (os.path.abspath(__file__), O.__file__)},
           "B1_references": 5 * len(J["bartlett"]), "B1_ecart_relatif_max": e1, "B2_taux": nb2,
           "B3_replications": n3, "B3_ecart_relatif_max": str(float(e3)), "tolerance_relative_B3": "1e-40",
           "B4_replications_recomptees": n4}
    with open(a.sortie, "xb") as f:
        f.write((json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
