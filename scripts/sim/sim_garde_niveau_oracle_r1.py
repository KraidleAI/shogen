"""SHOGEN-CRITERE-GARDE-NIVEAU-1 (partie 3 de S2, étape S), sous-lot S-b : oracle de sim_garde_niveau.py contre le
pré-enregistrement et contre r1 à HEAD (journal G1 docs/G1-partie-3-S.md §1.7).
(T0) cas de la sortie = table du journal (§1.3, §2), R = R0/diviseur ; g théorique recalculé en Fraction, ≥ g cible et
     à moins de 0,1 % au-dessus. (T1) invariants de la sortie (valeurs, classes de garde, conditionnels, indices,
     erreurs-types et écarts à 0,01 recalculés depuis x et D) ; invariants (4b) (ii) de sim_niveau_oracle_r1.
(T2) référence binomiale : k* exact en Fraction ; niveau contre r1.binomial_tail_ge, 10⁻⁴⁰ près en relatif.
(T3) par cas : r = 0..49, toutes les REJETTE, les 50 premières discordances et tous les rejets non qualifiables de
     la sortie, chacun de la valeur annoncée ; série régénérée par sim_niveau_oracle_r1.serie (sans sim_niveau_calc) :
     e, runs, K égaux ; N égal à r1.block_long_run_variance ; valeur égale au cas de r1.regle_critere ; P̂_more,
     garde, z, z_bloc à 10⁻⁴⁰ près en relatif.
Sortie ≠ 0 au premier écart (« ECHEC (Tk) »), aucun fichier ; sinon enregistrement JSON (mode xb, jamais d'écrasement).
Usage : python3.13 -B sim_garde_niveau_oracle_r1.py --r1 EXPORT/s2-harness --commit SHA --json garde_niveau.json
        --sortie FICHIER.json [--processus k]          Worker G1 claude-opus-5-5, 2026-10-02."""
import argparse, hashlib, json, math, multiprocessing, os, sys
from decimal import Decimal, localcontext
from fractions import Fraction

TABLE = ((1, 7200, "0.005107", 10, 30000), (1, 7200, "0.006279", 15, 30000), (1, 7200, "0.007274", 20, 30000),
         (1, 7200, "0.00896", 30, 30000), (1, 25000, "0.00272", 10, 30000), (1, 25000, "0.003338", 15, 30000),
         (1, 25000, "0.00386", 20, 30000), (1, 25000, "0.004741", 30, 30000),
         *((L, n, p, g, 6000) for L in (5, 20, 60) for n, p, g in ((7200, "0.005107", 10), (7200, "0.00896", 30),
                                                                    (25000, "0.00272", 10), (25000, "0.004741", 30))))
CAS_R1 = {"rejette": "REJETTE", "z_sous_seuil": "NE REJETTE PAS (z < 2,33)", "discordance": "NE REJETTE PAS (discordance)",
          "garde_5_4": "NON ÉVALUABLE (garde §5.4)", "rejet_non_qualifiable": "NON ÉVALUABLE (rejet non qualifiable)"}
CLASSES = (("[10 ; 12,5)", Decimal(10), Decimal("12.5")), ("[12,5 ; 15)", Decimal("12.5"), Decimal(15)),
           ("[15 ; 20)", Decimal(15), Decimal(20)), ("[20 ; 30)", Decimal(20), Decimal(30)), ("[30 ; +∞)", Decimal(30), None))
TOL, N_FLUX, W = Fraction(1, 10 ** 40), 11, 60
r1 = C = O = None


def echec(t, msg):
    sys.exit(f"ECHEC ({t}) : {msg}")


def contexte():
    """Contexte Decimal de r1 : objet CONTEXTE_DECIMAL à 3414e0f, fabrique contexte_decimal() après le lot P3
    (SHOGEN-CONTEXTE-MUTABLE-1) ; mêmes valeurs. Aucun alias n'est ajouté à r1."""
    return r1.contexte_decimal() if hasattr(r1, "contexte_decimal") else r1.CONTEXTE_DECIMAL


def pmore(p):
    pf = Fraction(float(p))
    return 1 - (1 - pf) ** N_FLUX - N_FLUX * pf * (1 - pf) ** (N_FLUX - 1)


def ecart_rel(x, y):
    fx, fy = Fraction(x), Fraction(y)
    return abs(fx - fy) / abs(fx) if fx else abs(fy)


def taux_ok(u, x, D):
    """(T1) x, r, SE et borne d'un taux recalculés depuis x et D (formules du journal §1.6)."""
    r = x / D
    return (u["x"] == x and u["r"] == r and math.isclose(u["SE"], math.sqrt(r * (1 - r) / D), rel_tol=1e-12, abs_tol=0)
            and u["borne95_si_x_nul"] == (1 - 0.05 ** (1 / D) if x == 0 else None))


def invariants(c, R):
    k, V, cl, t = c["comptes"], list(CAS_R1.values()), c["classes_garde"], c["garde_tenue"]
    i, ct, lec = c["indices"], c["conditionnels_garde_tenue"], c["lecture"]
    regles = [("Σ valeurs = R", sum(c["valeurs"][v]["x"] for v in V) == R),
              ("valeurs : x et SE", all(taux_ok(c["valeurs"][v], k[v], R) for v in V)),
              ("trois valeurs du pt 5", [c["valeurs_pt5"][v]["x"] for v in ("REJETTE", "NE REJETTE PAS", "NON ÉVALUABLE")]
               == [k[V[0]], k[V[1]] + k[V[2]], k[V[3]] + k[V[4]]]),
              ("garde tenue = R − garde non tenue", t == R - k["garde non tenue"]),
              ("Σ m des classes = garde tenue", sum(x["m"] for x in cl) == t),
              ("Σ z ≥ 2,33 des classes = comptes", sum(x["z"]["x"] for x in cl if x["m"]) == k["z ≥ 2,33"]),
              ("Σ REJETTE, discordance, non qualifiable des classes",
               [sum(x[v]["x"] for x in cl if x["m"]) for v in (V[0], V[2], V[4])] == [k[V[0]], k[V[2]], k[V[4]]]),
              ("taux des classes", all(taux_ok(x[v], x[v]["x"], x["m"]) for x in cl if x["m"]
                                       for v in ("z", V[0], V[2], V[4]))),
              ("ĝ de chaque classe dans ses bornes", [x["classe"] for x in cl] == [nom for nom, _, _ in CLASSES]
               and all(lo <= Decimal(x["g_min_max"][0]) <= Decimal(x["g_min_max"][1])
                       and (hi is None or Decimal(x["g_min_max"][1]) < hi) if x["m"] else x["g_min_max"] == []
                       for x, (_, lo, hi) in zip(cl, CLASSES))),
              ("conditionnels", ct == {"z": None, "regle": None} if t == 0 else
               taux_ok(ct["z"], k["z ≥ 2,33"], t) and taux_ok(ct["regle"], k[V[0]], t)),
              ("indices", len(i["REJETTE"]) == k[V[0]] and len(i["rejet_non_qualifiable"]) == k[V[4]]
               and len(i["discordance_50_premieres"]) == min(50, k[V[2]])),
              ("indices croissants et < R", all(a < b for l in i.values() for a, b in zip(l, l[1:]))
               and all(0 <= x < R for l in i.values() for x in l)),
              ("lecture", all(lec[nom] == (None if u is None or u["SE"] == 0 else (u["r"] - 0.01) / u["SE"]) for nom, u in
                              (("r_z", c["taux"]["z"]), ("r_z_t", ct["z"]), ("r_regle", c["taux"]["regle"]),
                               ("r_regle_t", ct["regle"]))))]
    for nom, ok in regles:
        if not ok:
            echec("T1", f"{nom}, L={c['L']} n={c['n']} p={c['p']}")
    return len(regles)


def verifier(args):
    """(T3) Une réplication : rend (écarts relatifs maximaux, P̂_more égal à l'identique) ou le message d'échec."""
    p, L, n, r, attendue = args
    d, (e, runs, I) = C.replication(p, L, n, r), O.serie(p, L, n, r)
    t = f"p={p!r} L={L} n={n} r={r}"
    if attendue is not None and d["valeur"] != attendue:
        return f"ECHEC (T3) : indice de la sortie de valeur {attendue}, réplication de valeur {d['valeur']}, {t}"
    if (e, runs, sum(I)) != (d["e"], d["runs"], d["K"]):
        return f"ECHEC (T3) : e, runs ou K, {t}"
    serie = [(W * j, x) for j, x in enumerate(I)]
    if r1.block_long_run_variance(serie, W)["numerateur"] != d["N"]:
        return f"ECHEC (T3) : N contre r1.block_long_run_variance, {t}"
    with localcontext(contexte()):
        phats = [+(Decimal(x) / Decimal(n)) for x in e]                       # r1.compute_r1 à HEAD
    pm = r1.poisson_binomial(phats)[2]
    gate = r1.gate_value(n, pm)
    z = None if r1.insufficient_history(n, pm) else r1.z_score(n, d["K"], pm)
    bloc = r1.bloc_strate(serie, W, pm, gate)
    cas = r1.regle_critere({"strates": {"s": {"z": z, "bloc": bloc, "gate_value": gate, "n": n}}})["strates"]["s"]["cas"]
    if CAS_R1[cas] != d["valeur"]:
        return f"ECHEC (T3) : valeur {d['valeur']} contre r1.regle_critere {cas}, {t}"
    ec = {}
    for nom, x, y in (("P_more", pm, d["P_more"]), ("garde", gate, d["garde"]), ("z", z, d["z"]),
                      ("z_bloc", bloc["z_bloc"], d["z_bloc"])):
        if (x is None) != (y is None) or (x is not None and ecart_rel(x, y) > TOL):
            return f"ECHEC (T3) : {nom}, r1 {x}, script {y}, {t}"
        ec[nom] = ecart_rel(x, y) if x is not None else Fraction(0)
    return ec, pm == d["P_more"]


def main():
    global r1, C, O
    ap = argparse.ArgumentParser(description="oracle S-b de SHOGEN-CRITERE-GARDE-NIVEAU-1")
    for nom in ("--r1", "--commit", "--json", "--sortie"):
        ap.add_argument(nom, required=True)
    ap.add_argument("--processus", type=int, default=1)
    a = ap.parse_args()
    if os.path.exists(a.sortie):
        sys.exit("refus : le fichier de sortie existe deja")
    sys.path[:0] = [os.path.dirname(os.path.abspath(__file__)), os.path.abspath(a.r1)]
    import sim_niveau_calc as C, sim_niveau_oracle_r1 as O
    from shogen_s2 import r1
    J = json.loads(open(a.json, "rb").read().decode("utf-8"))
    dv, cas = J["parametres"]["diviseur"], J["cas"]
    if [(c["L"], c["n"], c["p"], c["g_cible"], c["comptes"]["R"]) for c in cas] != [
            (L, n, p, g, R0 // dv) for L, n, p, g, R0 in TABLE] or J["parametres"]["cas"] != [list(x) for x in TABLE]:
        echec("T0", "cas de la sortie différents de la table du journal (§1.3, §2)")
    for c in cas:
        g = c["n"] * pmore(c["p"]) * (1 - pmore(c["p"]))
        if not (c["g_cible"] <= g < Fraction(1001, 1000) * c["g_cible"] and c["g_theorique"] == float(g)):
            echec("T0", f"g théorique {float(g)}, L={c['L']} n={c['n']} p={c['p']}")
    n1 = sum(invariants(c, c["comptes"]["R"]) for c in cas)
    n4b = O.invariants(a.json)[1]
    e2 = Fraction(0)
    for c in cas:
        P, ref = pmore(c["p"]), c["reference_iid_P_connu"]
        m, v, k = c["n"] * P, c["n"] * P * (1 - P), math.ceil(c["n"] * P)
        while (k - m) ** 2 < Fraction(233, 100) ** 2 * v:
            k += 1
        with localcontext(contexte()):
            Pd = Decimal(P.numerator) / Decimal(P.denominator)
        e2 = max(e2, ecart_rel(r1.binomial_tail_ge(k, c["n"], Pd), Decimal(ref["niveau"])))
        if ref["k_etoile"] != k or e2 > TOL or Decimal(ref["P_more"]) != Pd:
            echec("T2", f"k* {ref['k_etoile']} contre {k}, ou niveau, L={c['L']} n={c['n']} p={c['p']}")
    taches = []
    for c in cas:
        att = {r: v for cle, v in zip(("REJETTE", "discordance_50_premieres", "rejet_non_qualifiable"),
                                       (CAS_R1["rejette"], CAS_R1["discordance"], CAS_R1["rejet_non_qualifiable"]))
               for r in c["indices"][cle]}
        R = c["comptes"]["R"]
        taches += [(float(c["p"]), c["L"], c["n"], r, att.get(r)) for r in sorted(set(range(min(50, R))) | set(att))]
    with multiprocessing.get_context("fork").Pool(a.processus) as pool:
        res = pool.map(verifier, taches, 4)
    for x in res:
        if isinstance(x, str):
            sys.exit(x)
    emax = {k: str(float(max(ec[k] for ec, _ in res))) for k in ("P_more", "garde", "z", "z_bloc")}
    b = open(r1.__file__, "rb").read()
    rec = {"oracle": "S-b SHOGEN-CRITERE-GARDE-NIVEAU-1 : table du journal, invariants, référence, r1 à HEAD",
           "commit_r1": a.commit, "blob_r1": hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest(),
           "sha256_r1": hashlib.sha256(b).hexdigest(), "json": os.path.basename(a.json),
           "sha256_json": hashlib.sha256(open(a.json, "rb").read()).hexdigest(),
           "script_sha256": {os.path.basename(f): hashlib.sha256(open(f, "rb").read()).hexdigest()
                             for f in (os.path.abspath(__file__), C.__file__, O.__file__)},
           "T0_cas": len(cas), "T1_invariants": n1, "T1_invariants_4b_ii": n4b, "T2_ecart_relatif_max": str(float(e2)),
           "T3_replications": len(res), "T3_P_more_egaux_a_l_identique": sum(eg for _, eg in res),
           "T3_ecart_relatif_max": emax, "tolerance_relative": "1e-40"}
    with open(a.sortie, "xb") as f:
        f.write((json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
