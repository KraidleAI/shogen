"""SHOGEN-SIM-NIVEAU-MODELES-1, SHOGEN-FLUX-QUASI-MORT-2 et SHOGEN-FLUX-FAIBLE-1 (lot DETTES-SIM) : oracle de sim_modeles.py
et de sim_flux.py, écrit avant eux. (M0) cas et profils = tables du pré-enregistrement, recopiées ici ; R/diviseur ;
alternative (q, p′, c) ; paramètres des extensions (trous, α, p_i, L mêlé, d0 ; correction C-2 du G2).
(M1) invariants (4b) (ii) de sim_niveau_oracle_r1 ; taux recalculés depuis x et R.
(M2) FLUX : P_more et excès espéré exact recalculés par un autre algorithme (convolution des lois de 0 et 1 écart,
     au lieu des sommes de produits du générateur), (n − 1)·c·(P(M = 0) − P(M = 1)) sur les flux hors de la paire,
     c depuis la table 2×2 de la paire ; 10⁻¹² près en relatif ; bascule exacte (1 − 9p)/(2 − 10p) ; bascule mesurée
     refaite depuis les moyennes publiées (premier changement de signe, interpolation linéaire).
(M3) premières réplications publiées (controle_premieres) : série régénérée par sim_dettes_calc, comptes refaits par
     boucles simples (sans masques de bits), puis r1 : p̂_i, poisson_binomial, gate_value, insufficient_history,
     z_score, bloc_strate (fenêtres présentes, w = 60 s), regle_critere ; n, K, e, N égaux ; P_more, z, z_bloc à 10⁻⁴⁰.
(M4, --complet, pour les exécutions réduites) : toutes les réplications refaites (sim_dettes_calc) et comptées par un
code distinct de sim_dettes_calc.compter ; égalité exacte des comptes. Sortie ≠ 0 au premier écart, aucun fichier ;
sinon enregistrement JSON (mode xb).
Usage : python3.13 -B sim_dettes_oracle_r1.py --r1 EXPORT/s2-harness --commit SHA --modeles F.json --flux F.json
--sortie F.json      Worker G1 DETTES-SIM, claude-opus-5-5, 2026-10-04."""
import argparse, hashlib, json, math, os, sys
from decimal import Decimal, localcontext
from fractions import Fraction

MODELES = (*(("a", L, T) for L in (1, 20, 60) for T in (11112, 27778)),
           *(("b", L, n) for L in ("1", "20", "mele") for n in (10000, 25000)),
           *(("c", L, n) for L in (5, 20, 60) for n in (10000, 25000)))
G13 = (0, 0.1, 0.2, 0.25, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.75, 0.9, 1)
PROFILS = ((0, None), *((1, w) for w in G13), *((k, w) for k in (2, 4) for w in (0.1, 0.25, 0.4)))
R_MO, R_FX, N_FX, P, Q, W, TOL = 4000, 4000, 10000, 0.02, 0.006667, 60, Fraction(1, 10 ** 40)
EXT = {"trou": [0.1, 60], "alpha": 1.5, "hetero": [0.01] * 6 + [0.04] * 5, "mele": [1, 5, 20, 60] * 2 + [1, 5, 20]}
D0 = {"5": 2.22263, "20": 9.7436, "60": 29.7479}                  # pré-enregistrement §1, extensions (a), (b), (c)


def echec(t, msg):
    sys.exit(f"ECHEC ({t}) : {msg}")


def taux(u, x, R):
    r = x / R
    return (u["x"] == x and u["r"] == r and math.isclose(u["SE"], math.sqrt(r * (1 - r) / R), rel_tol=1e-12, abs_tol=0)
            and u["borne95_si_x_nul"] == (1 - 0.05 ** (1 / R) if x == 0 else None))


def ecart_rel(x, y):
    fx, fy = Fraction(x), Fraction(y)
    return abs(fx - fy) / abs(fx) if fx else abs(fy)


def p01(taux_):
    """(P(M = 0), P(M = 1)) du nombre M d'écarts de flux indépendants, par convolution."""
    d0, d1 = Fraction(1), Fraction(0)
    for x in map(Fraction, taux_):
        d0, d1 = d0 * (1 - x), d1 * (1 - x) + d0 * x
    return d0, d1


def taux_profil(k, w):
    return [P, P] + [P if (k == 0 or j >= k) else w for j in range(9)]


def verifier(r1, flux, pres, rec, t):
    """(M3) une réplication publiée contre r1 ; comptes par boucles simples ; rend les écarts relatifs."""
    T = len(flux[0])
    pres = pres if pres is not None else [1] * T
    tp = [i for i in range(T) if pres[i]]
    e = [sum(d[i] for i in tp) for d in flux]
    I = [int(sum(d[i] for d in flux) >= 2) for i in tp]
    n, K = len(tp), sum(I)
    serie = [(W * i, x) for i, x in zip(tp, I)]
    N = r1.block_long_run_variance(serie, W)["numerateur"]
    if (n, K, e, N) != (rec["n"], rec["K"], rec["e"], rec["N"]):
        echec("M3", f"n, K, e ou N, {t}")
    with localcontext(r1.contexte_decimal()):
        ph = [+(Decimal(x) / Decimal(n)) for x in e]
    pm = r1.poisson_binomial(ph)[2]
    gate = r1.gate_value(n, pm)
    z = None if r1.insufficient_history(n, pm) else r1.z_score(n, K, pm)
    bloc = r1.bloc_strate(serie, W, pm, gate)
    cas = r1.regle_critere({"strates": {"s": {"z": z, "bloc": bloc, "gate_value": gate, "n": n}}})["strates"]["s"]["cas"]
    lib = {"rejette": "REJETTE", "z_sous_seuil": "NE REJETTE PAS (z < 2,33)", "discordance": "NE REJETTE PAS (discordance)",
           "garde_5_4": "NON ÉVALUABLE (garde §5.4)", "rejet_non_qualifiable": "NON ÉVALUABLE (rejet non qualifiable)"}
    if lib[cas] != rec["valeur"]:
        echec("M3", f"valeur {rec['valeur']} contre r1.regle_critere {cas}, {t}")
    out = []
    for nom, x, y in (("P_more", pm, rec["P_more"]), ("z", z, rec["z"]), ("z_bloc", bloc["z_bloc"], rec["z_bloc"])):
        if (x is None) != (y is None) or (x is not None and ecart_rel(x, Decimal(y)) > TOL):
            echec("M3", f"{nom} : r1 {x}, sortie {y}, {t}")
        out.append(ecart_rel(x, Decimal(y)) if x is not None else Fraction(0))
    return max(out)


def compte(ds, cles):
    """(M4) comptes d'une liste d'enregistrements de sim_dettes_calc.stats, code distinct de compter()."""
    c, s = dict.fromkeys(cles, 0), Decimal("2.33")
    for d in ds:
        z, zb = d["z"], d["z_bloc"]
        for cle, ok in (("garde non tenue", not d["tenue"]), ("σ̂² = 0", d["N"] == 0), ("z_bloc non publiée", zb is None),
                        ("z ≥ 2,33", z is not None and z >= s), ("z_bloc ≥ 2,33", zb is not None and zb >= s),
                        (d["valeur"], True), ("z ≤ −2,33", z is not None and z <= -s),
                        ("z_bloc ≤ −2,33", zb is not None and zb <= -s), ("run maximal de I ≥ ℓ", d["rmax"] >= 240)):
            c[cle] += ok
    return c


def complet(D3, M, F, Rm, Rf):
    cles = [k for k in M["cas"][0]["comptes"] if k != "R"]
    for cs in M["cas"]:
        if compte([D3.stats(*D3.serie_modele(tuple(cs["cas"]), r)) for r in range(Rm)], cles) != {
                k: cs["comptes"][k] for k in cles}:
            echec("M4", f"comptes du cas {cs['cas']}")
    ds = [[] for _ in F["cas"]]
    for r in range(Rf):
        U, cache = D3.base_flux(N_FX, r), {}
        for j, cs in enumerate(F["cas"]):
            ds[j].append(D3.stats(D3.profil(U, taux_profil(cs["k"], cs["p_w"]), Q if cs["alternative"] else 0, cache), None))
    for cs, d in zip(F["cas"], ds):
        if compte(d, cles) != {k: cs["comptes"][k] for k in cles}:
            echec("M4", f"comptes du profil {cs['k'], cs['p_w'], cs['alternative']}")
    return len(M["cas"]) * Rm + Rf


def main():
    ap = argparse.ArgumentParser(description="oracle de SHOGEN-SIM-NIVEAU-MODELES-1, -FLUX-QUASI-MORT-2, -FLUX-FAIBLE-1")
    for nom in ("--r1", "--commit", "--modeles", "--flux", "--sortie"):
        ap.add_argument(nom, required=True)
    ap.add_argument("--complet", action="store_true")
    a = ap.parse_args()
    if os.path.exists(a.sortie):
        sys.exit("refus : le fichier de sortie existe deja")
    sys.path[:0] = [os.path.dirname(os.path.abspath(__file__)), os.path.abspath(a.r1)]
    import sim_dettes_calc as D3, sim_niveau_oracle_r1 as O
    from shogen_s2 import r1
    M, F = (json.loads(open(f, "rb").read().decode("utf-8")) for f in (a.modeles, a.flux))
    Rm, Rf = R_MO // M["parametres"]["diviseur"], R_FX // F["parametres"]["diviseur"]
    if [tuple(c["cas"]) for c in M["cas"]] != list(MODELES) or any(c["comptes"]["R"] != Rm for c in M["cas"]):
        echec("M0", "cas de sim_modeles différents du pré-enregistrement")
    pm_ = M["parametres"]
    if any(pm_[k] != v for k, v in EXT.items()) or {k: v[0] for k, v in pm_["lourd_d0_ED"].items()} != D0:
        echec("M0", "paramètres des extensions de sim_modeles différents du pré-enregistrement")
    pf = F["parametres"]
    if [(c["k"], c["p_w"], c["alternative"]) for c in F["cas"]] != [(k, w, al) for k, w in PROFILS for al in (False, True)] \
            or (pf["n"], pf["q"], pf["p"]) != (N_FX, Q, P) or any(c["comptes"]["R"] != Rf for c in F["cas"]):
        echec("M0", "profils, n, q ou p de sim_flux différents du pré-enregistrement")
    qf, pp = Fraction(Q), Fraction((P - Q) / (1 - Q))
    c = (qf + (1 - qf) * pp * pp) - (qf + (1 - qf) * pp) ** 2
    if pf["p_prime"] != (P - Q) / (1 - Q) or abs(Fraction(pf["c"]) / c - 1) > Fraction(1, 10 ** 12):
        echec("M0", "p′ ou c de l'alternative")
    n1 = O.invariants(a.modeles)[1] + O.invariants(a.flux)[1]
    for J, R in ((M, Rm), (F, Rf)):
        for cs in J["cas"]:
            if not all(taux(cs["taux"][k], cs["taux"][k]["x"], R) for k in ("z", "z_bloc", "regle")):
                echec("M1", f"taux, cas {cs.get('cas') or (cs['k'], cs['p_w'])}")
    e2 = Fraction(0)
    for cs in F["cas"]:
        ps = taux_profil(cs["k"], cs["p_w"])
        pmo, (m0, m1) = 1 - sum(p01(ps)), p01(ps[2:])
        ex = (N_FX - 1) * c * (m0 - m1) if cs["alternative"] else Fraction(0)
        for nom, x, y in (("P_more_marges", pmo, cs["exact"]["P_more_marges"]), ("exces", ex, cs["exact"]["exces"])):
            d = abs(Fraction(y) - x) / (abs(x) if x else 1)
            e2 = max(e2, d)
            if d > Fraction(1, 10 ** 12):
                echec("M2", f"{nom} : oracle {float(x)!r}, sortie {y!r}, profil {cs['k'], cs['p_w'], cs['alternative']}")
    if abs(F["bascule"]["exacte"] - (1 - 9 * P) / (2 - 10 * P)) > 1e-12:
        echec("M2", "bascule exacte")
    al = [(cs["p_w"], cs["mesure"]["exces_moyen"]) for cs in F["cas"] if cs["k"] == 1 and cs["alternative"]]
    br = next(((w1, w2, m1, m2) for (w1, m1), (w2, m2) in zip(al, al[1:]) if m1 > 0 >= m2), None)
    bm = None if br is None else br[0] + (br[1] - br[0]) * br[2] / (br[2] - br[3])
    if (bm is None) != (F["bascule"]["mesuree"] is None) or (bm is not None and abs(F["bascule"]["mesuree"] - bm) > 1e-12):
        echec("M2", f"bascule mesurée : sortie {F['bascule']['mesuree']}, oracle {bm}")
    e3, n3 = Fraction(0), 0
    for cs in M["cas"]:
        for rec in cs["controle_premieres"]:
            e3, n3 = max(e3, verifier(r1, *D3.serie_modele(tuple(cs["cas"]), rec["r"]), rec, f"{cs['cas']} r={rec['r']}")), n3 + 1
    U = {}
    for cs in F["cas"]:
        for rec in cs["controle_premieres"]:
            U.setdefault(rec["r"], D3.base_flux(N_FX, rec["r"]))
            fl = D3.profil(U[rec["r"]], taux_profil(cs["k"], cs["p_w"]), Q if cs["alternative"] else 0)
            e3, n3 = max(e3, verifier(r1, fl, None, rec, f"profil {cs['k'], cs['p_w'], cs['alternative']} r={rec['r']}")), n3 + 1
    n4 = complet(D3, M, F, Rm, Rf) if a.complet else 0
    b = open(r1.__file__, "rb").read()
    sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
    rec = {"oracle": "MODELES-1, FLUX-QUASI-MORT-2, FLUX-FAIBLE-1 : pré-enregistrement, invariants, exact, r1",
           "commit_r1": a.commit, "blob_r1": hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest(),
           "sha256_r1": hashlib.sha256(b).hexdigest(), "json": {f: sha(f) for f in (a.modeles, a.flux)},
           "script_sha256": {os.path.basename(f): sha(f) for f in (os.path.abspath(__file__), D3.__file__, O.__file__)},
           "M0_cas": len(M["cas"]), "M0_profils": len(F["cas"]), "M0_parametres_extensions": len(EXT) + 1,
           "M1_invariants_4b_ii": n1,
           "M2_ecart_relatif_max": str(float(e2)), "M3_replications": n3, "M3_ecart_relatif_max": str(float(e3)),
           "tolerance_relative_M3": "1e-40", "M4_replications_recomptees": n4}
    with open(a.sortie, "xb") as f:
        f.write((json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
