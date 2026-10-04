"""SHOGEN-BARTLETT-BIAIS-1 et SHOGEN-POOLEE-BLOC-1 (b) (lot DETTES-SIM, 2026-10-04), modèle nul synthétique de SIM-NIVEAU
(p = 0,02 ; L ∈ {1, 5, 20, 60}). Réplication r = paire de strates sans lien (n = 10⁴ et 2,5·10⁴) = réplications r des
cas de SIM-NIVEAU (sim_niveau_calc.replication, inchangée : mêmes octets). BARTLETT : σ̂²_bloc contre les références
exactes du modèle (R(k) de I_t, Var(K), n·σ²_∞, E[σ̂²_bloc] par la forme en lags centrée sur Ī, terme de premier ordre
de Künsch 1989, Thm 3.2 (i)) ; niveaux à P connu. POOLEE (b) : niveau de z_pool (D2 pt 4, publié si les deux gardes
sont tenues, r1.strate_poolee) et de la forme par blocs écrite en B.13 (a). Oracles internes : (2), (2b), moyennes et
variance contre la théorie à 5 SE (fail-closed) ; oracle externe : sim_bartlett_poolee_oracle.py.
Usage : python3.13 -B sim_bartlett_poolee.py --sortie DOSSIER [--processus k] [--diviseur d]   Worker G1 DETTES-SIM."""
import argparse, hashlib, math, os, sys, time
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import accumulate
from statistics import NormalDist

import sim_dettes_commun as D
import sim_niveau as S
import sim_niveau_calc as C

P, LS, NS, R0, DIV_PREFIXE, ELL = 0.02, (1, 5, 20, 60), (10000, 25000), 5000, 20, C.ELL
ITEM, S2 = "SHOGEN-BARTLETT-BIAIS-1 ; SHOGEN-POOLEE-BLOC-1 (b)", Fraction(233, 100) ** 2
CONSEQUENCE = ("Conséquence pré-déclarée (lot DETTES-SIM) : cette sortie ne modifie ni ℓ, ni le seuil, ni la règle, ni "
               "la strate poolée ; ajoutée après l'exécution unique ; synthétique ; hors décision. Rien n'est établi sur "
               "des sources réelles (doc 09).")


def rk(L, n):
    """R(k), k = 0..n − 1, de I_t = 1{m_t ≥ 2} (11 chaînes stationnaires indépendantes, a et b de sim_niveau_calc.chaine) :
    P(I_t = I_t+k = 1) = 1 − 2·P(m ≤ 1) + P(m_t ≤ 1 ∧ m_t+k ≤ 1) (cinq termes multinomiaux), moins P_more² ; R(k) = 0
    dès que λ^k < 10⁻²⁰ (k ≥ 1 ; L = 1 : λ = 0) : le bruit d'annulation cumulé dépasserait 10⁻⁹ en relatif (oracle B1)."""
    a, b = C.chaine(P, L)
    lam, q, out = a - b, 1 - P, []
    p1 = q ** 11 + 11 * P * q ** 10
    for k in range(n):
        g = lam ** k if k else 1.0
        if k and g < 1e-20:
            out.append(0.0)
            continue
        x11, x10 = P * (P + q * g), P * q * (1 - g)
        x00 = 1 - x11 - 2 * x10
        out.append(1 - 2 * p1 + x00 ** 11 + 11 * (2 * x10 + x11) * x00 ** 10 + 110 * x10 * x10 * x00 ** 9 - (1 - p1) ** 2)
    return out


def exactes(L, n):
    """E[γ̂_k] = (n − k)R(k) − (Σ_{t ≤ n−k} A(t) + Σ_{t > k} A(t))/n + (n − k)·Var(K)/n², A(t) = Σ_s R(s − t)."""
    R = rk(L, n)
    cum = list(accumulate([0.0] + R[1:]))
    pa = list(accumulate([0.0] + [R[0] + cum[t - 1] + cum[n - t] for t in range(1, n + 1)]))
    vk = pa[n]
    eg = [(n - k) * R[k] - (pa[n - k] + pa[n] - pa[k]) / n + (n - k) * vk / (n * n) for k in range(ELL)]
    return {"var_K_exacte": vk, "n_sigma2_inf": n * math.fsum([R[0]] + [2 * x for x in R[1:]]),
            "E_sigma2_bloc_exacte": math.fsum([eg[0]] + [2 * (1 - k / ELL) * eg[k] for k in range(1, ELL)]),
            "E_centre_sur_P": math.fsum([n * R[0]] + [2 * (1 - k / ELL) * (n - k) * R[k] for k in range(1, ELL)]),
            "kunsch_premier_ordre": -n / ELL * math.fsum(2 * k * R[k] for k in range(1, n))}


def tache(args):
    """Réplication r : les deux strates, sim_niveau_calc.replication inchangée ; (2) et (2b) exigés."""
    L, r = args
    out = []
    for n in NS:
        d = C.replication(P, L, n, r)
        if not (d["ok2"] and d["ok2b"]):
            raise RuntimeError(f"oracle (2) ou (2b) en echec : L={L} n={n} r={r}")
        out.append((n, d["K"], d["N"], d["P_more"], d["tenue"], d["z"], d["z_bloc"], d["ligne"]))
    return out


def agreger(L, R, recs, ex):
    pf = Fraction(P)
    pm = 1 - (1 - pf) ** 11 - 11 * pf * (1 - pf) ** 10
    h, hp, st, pool = hashlib.sha256(), hashlib.sha256(), {n: {"s2": [], "K": [], "X": [], "c": [0] * 5} for n in NS}, {
        "zp": [], "zb": [], "c": [0, 0, 0, 0, 0], "ctl": []}
    for r, rec in enumerate(recs):
        num, s2s, tenues = Decimal(0), Decimal(0), True
        for n, K, N, pm_, ten, z, zb, ligne in rec:
            h.update(ligne.encode("utf-8"))
            if r < R // DIV_PREFIXE:
                hp.update(ligne.encode("utf-8"))
            s, d = st[n], K - n * pm
            s["s2"].append(N / (ELL * n * n))
            s["K"].append(K)
            with localcontext() as ctx:
                ctx.prec = C.PREC
                x = Decimal(K) - Decimal(n) * pm_
                num, s2s = +(num + x), +(s2s + Decimal(N) / Decimal(ELL * n * n))
            s["X"].append(float(x))
            vrai = (d >= 0 and d * d >= S2 * n * pm * (1 - pm), N > 0 and n >= C.N_MIN_BLOCS and d >= 0
                    and d * d >= S2 * Fraction(N, ELL * n * n), d >= 0 and d * d >= S2 * Fraction(ex[n]["var_K_exacte"]),
                    z is not None and z >= C.SEUIL_Z, zb is not None and zb >= C.SEUIL_Z)
            s["c"] = [u + v for u, v in zip(s["c"], vrai)]
            tenues = tenues and ten
        with localcontext() as ctx:
            ctx.prec = C.PREC
            var = sum((Decimal(n) * p_ * (1 - p_) for n, _, _, p_, *_ in rec), Decimal(0))
            zp = +(num / var.sqrt()) if tenues else None
            zb = +(num / s2s.sqrt()) if all(N > 0 for _, _, N, *_ in rec) else None
        for v, z in ((pool["zp"], zp), (pool["zb"], zb)):
            if z is not None:
                v.append(float(z))
        pool["c"] = [u + v for u, v in zip(pool["c"], (zp is not None and zp >= C.SEUIL_Z, zb is not None and
                     zb >= C.SEUIL_Z, zp is not None and zb is not None and min(zp, zb) >= C.SEUIL_Z, zp is not None,
                     zb is not None))]
        if r < 20:
            pool["ctl"].append([None if zp is None else str(zp), None if zb is None else str(zb)])
    cas = []
    for n in NS:
        s, e = st[n], ex[n]
        (ms, ses), (mk, sek), (mx, sex) = D.moy_se(s["s2"]), D.moy_se(s["K"]), D.moy_se(s["X"])
        vK, vX = sek * sek * R, sex * sex * R
        dv = [(k - mk) ** 2 for k in s["K"]]
        o = [D.controle("moyenne de σ̂²_bloc contre E exacte", ms, e["E_sigma2_bloc_exacte"], ses),
             D.controle("moyenne de K contre n·P_more", mk, float(n * pm), sek),
             D.controle("variance de K contre Var(K) exacte", vK, e["var_K_exacte"], S.moy_sd(dv)[1] / math.sqrt(R))]
        V = e["var_K_exacte"]
        cas.append({"L": L, "n": n, "exact": e, "relatifs_exacts": {
            "biais": e["E_sigma2_bloc_exacte"] / V - 1, "poids_troncature": e["E_centre_sur_P"] / V - 1,
            "centrage": (e["E_sigma2_bloc_exacte"] - e["E_centre_sur_P"]) / V,
            "kunsch_premier_ordre_sur_n_sigma2_inf": e["kunsch_premier_ordre"] / e["n_sigma2_inf"]},
            "mesure": {"sigma2_moyenne": ms, "sigma2_SE": ses, "biais_relatif": ms / V - 1, "biais_relatif_SE": ses / V,
                       "var_K": vK, "var_X_plugin": vX, "E_sigma2_sur_var_X": e["E_sigma2_bloc_exacte"] / vX,
                       "X_moyen": mx},
            "taux": {k: S.taux(x, R) for k, x in zip(("z_P_connu", "z_bloc_P_connu", "z_var_exacte", "z_plugin",
                                                      "z_bloc_plugin"), s["c"])}, "oracles_internes": o})
    (a1, s1), (a2, s2_) = S.moy_sd(pool["zp"]), S.moy_sd(pool["zb"])
    c = pool["c"]
    return cas, {"L": L, "taux": {k: S.taux(x, R) for k, x in zip(("z_pool", "z_pool_bloc", "min"), c[:3])},
                 "publies": {"z_pool": c[3], "z_pool_bloc": c[4]}, "z_pool_moyenne": a1, "z_pool_sd": s1,
                 "z_pool_bloc_moyenne": a2, "z_pool_bloc_sd": s2_, "controle_premieres": pool["ctl"],
                 "empreinte_sha256": h.hexdigest(), "prefixe_R": R // DIV_PREFIXE, "empreinte_prefixe": hp.hexdigest()}


def texte(ent):
    f, tx = (lambda v: "—" if v is None else f"{v:+.4f}"), (lambda u: f"{u['x']} → {u['r']:.5f} (SE {u['SE']:.5f})" + (
        f" [borne 95 % {u['borne95_si_x_nul']:.2e}]" if u["x"] == 0 else ""))
    t = [f"{ITEM} ({ent['schema']}) ; " + " ; ".join(f"{k} sha256 {v}" for k, v in ent["script_sha256"].items()),
         f"Modèle de SIM-NIVEAU, p = {P}, R = {ent['parametres']['R']} par L ; réplication r = réplications r des cas "
         f"(L, 10⁴) et (L, 2,5·10⁴) de SIM-NIVEAU ; ℓ = {ELL} ; seuil 2,33 ; α nominal {ent['alpha_nominal']:.8f}.",
         ent["consequence_predeclaree"],
         "BARTLETT — L | n | Var(K) exacte | E[σ̂²] exacte | biais relatif exact (poids et troncature ; centrage) | "
         "biais mesuré (SE) | Künsch 1er ordre / nσ²_∞ | E[σ̂²]/Var(K − nP̂) | taux : z à P connu ; z_bloc à P "
         "connu ; z à Var(K) exacte ; z plug-in ; z_bloc plug-in"]
    for c in ent["bartlett"]:
        e, x, m, u = c["exact"], c["relatifs_exacts"], c["mesure"], c["taux"]
        t.append(f"{c['L']} | {c['n']} | {e['var_K_exacte']:.3f} | {e['E_sigma2_bloc_exacte']:.3f} | {f(x['biais'])} "
                 f"({f(x['poids_troncature'])} ; {f(x['centrage'])}) | {f(m['biais_relatif'])} ({m['biais_relatif_SE']:.4f})"
                 f" | {f(x['kunsch_premier_ordre_sur_n_sigma2_inf'])} | {m['E_sigma2_sur_var_X']:.4f} | "
                 + " ; ".join(tx(u[k]) for k in u))
    t.append("POOLEE (b) — L | publiés z_pool ; forme par blocs | r(z_pool ≥ 2,33) | r(forme par blocs ≥ 2,33) | "
             "r(les deux) | moyenne et SD de z_pool | empreinte")
    for c in ent["poolee"]:
        u = c["taux"]
        t.append(f"{c['L']} | {c['publies']['z_pool']} ; {c['publies']['z_pool_bloc']} | {tx(u['z_pool'])} | "
                 f"{tx(u['z_pool_bloc'])} | {tx(u['min'])} | {f(c['z_pool_moyenne'])} ; {f(c['z_pool_sd'])} | "
                 f"{c['empreinte_sha256']} ; préfixe {c['prefixe_R']} {c['empreinte_prefixe']}")
    return "\n".join(t) + "\n"


def main():
    ap = argparse.ArgumentParser(description=ITEM + " (lot DETTES-SIM)")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--processus", type=int, default=1)
    ap.add_argument("--diviseur", type=int, default=1)
    a = ap.parse_args()
    ch = D.chemins(a.sortie, "bartlett_poolee")
    sh = D.shas(os.path.abspath(__file__), D.__file__, S.__file__, C.__file__)
    R, debut, journal, bart, pool = R0 // a.diviseur, time.gmtime(), [], [], []
    with D.pool(a.processus) as pl:
        for L in LS:
            t0, ex = time.perf_counter(), {n: exactes(L, n) for n in NS}
            try:
                b, p = agreger(L, R, D.imap(pl, tache, ((L, r) for r in range(R)), 10), ex)
            except RuntimeError as exc:
                sys.exit(f"ECHEC D'ORACLE, aucun fichier ecrit : {exc}")
            bart, pool = bart + b, pool + [p]
            journal.append(f"L={L} R={R} : {time.perf_counter() - t0:.1f} s (horloge murale)")
            print(journal[-1], file=sys.stderr, flush=True)
    ent = {"schema": "shogen.sim-bartlett-poolee.v1", "item": ITEM, "script_sha256": sh,
           "journal": "docs/G1-lot-DETTES-SIM.md, pré-enregistrement", "etiquette": D.ETIQUETTE,
           "parametres": {"p": repr(P), "L": list(LS), "n": list(NS), "R": R, "diviseur": a.diviseur, "ell": ELL,
                          "seuil_z": str(C.SEUIL_Z), "garde_seuil": str(C.SEUIL_HIST), "garde_blocs_n_min": C.N_MIN_BLOCS,
                          "graine": C.GRAINE, "chaine_graine": C.CHAINE, "decimal_prec": C.PREC,
                          "prefixe": f"R/{DIV_PREFIXE}"},
           "alpha_nominal": 1 - NormalDist().cdf(2.33), "consequence_predeclaree": CONSEQUENCE, "bartlett": bart,
           "poolee": pool}
    D.ecrire(ch, ent, texte(ent), a.processus, debut, journal)


if __name__ == "__main__":
    main()
