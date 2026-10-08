"""SHOGEN-GARDE-NIVEAU-N-1 (lot DETTES-SIM) : oracle de sim_garde_n.py contre le pré-enregistrement du lot et contre r1
(export `git archive`), écrit avant le générateur ; aussi (T3) des sorties de SHOGEN-SIM-NIVEAU-P-1 (sim_niveau.py --p).
(T0) cas de la sortie = table du pré-enregistrement, R = R0/diviseur ; g théorique en Fraction, ≥ g cible, < 1,001·g.
(T1) invariants de chaque cas (sim_garde_niveau_oracle_r1.invariants) et (4b) (ii) (sim_niveau_oracle_r1.invariants).
(T2) référence binomiale : k* exact en Fraction ; niveau contre r1.binomial_tail_ge, 10⁻⁴⁰ près en relatif.
(T3) r = 0..49, toutes les REJETTE, les 50 premières discordances et tous les rejets non qualifiables, chacun de la
     valeur annoncée : sim_garde_niveau_oracle_r1.verifier (série régénérée sans sim_niveau_calc ; r1.regle_critere).
(T4) n < 30·ℓ (déduction de l'étape S §1.2) : REJETTE = discordance = 0, z_bloc non publiée = R, rejet non
     qualifiable = #{garde tenue ∧ z ≥ 2,33}.
--p1 F... : T3 sur r = 0..9 de chaque cas, plus (4b) (ii). Sortie ≠ 0 au premier écart, aucun fichier ; sinon
enregistrement JSON (mode xb). Usage : python3.13 -B sim_garde_n_oracle_r1.py --r1 EXPORT/s2-harness --commit SHA
--json garde_n.json --sortie F.json [--p1 sim_niveau.json ...] [--processus k]   Worker G1 DETTES-SIM, 2026-10-04."""
import argparse, hashlib, json, math, multiprocessing, os, sys
from decimal import Decimal, localcontext
from fractions import Fraction

GRILLE = ((2880, "0.008157", 10), (2880, "0.01006", 15), (2880, "0.01168", 20), (2880, "0.01445", 30),
          (5760, "0.005721", 10), (5760, "0.007038", 15), (5760, "0.008157", 20), (5760, "0.01006", 30))
TABLE = (*((1, n, p, g, 30000) for n, p, g in GRILLE),
         *((L, n, p, g, 6000) for L in (5, 20, 60) for n, p, g in GRILLE if g in (10, 30)))
ELL = 240


def echec(t, msg):
    sys.exit(f"ECHEC ({t}) : {msg}")


def main():
    ap = argparse.ArgumentParser(description="oracle de SHOGEN-GARDE-NIVEAU-N-1 (lot DETTES-SIM)")
    for nom in ("--r1", "--commit", "--json", "--sortie"):
        ap.add_argument(nom, required=True)
    ap.add_argument("--p1", nargs="*", default=[])
    ap.add_argument("--processus", type=int, default=1)
    a = ap.parse_args()
    if os.path.exists(a.sortie):
        sys.exit("refus : le fichier de sortie existe deja")
    sys.path[:0] = [os.path.dirname(os.path.abspath(__file__)), os.path.abspath(a.r1)]
    import sim_niveau_calc as C, sim_niveau_oracle_r1 as O, sim_garde_niveau_oracle_r1 as GO
    from shogen_s2 import r1
    GO.r1, GO.C, GO.O = r1, C, O
    J = json.loads(open(a.json, "rb").read().decode("utf-8"))
    dv, cas = J["parametres"]["diviseur"], J["cas"]
    if [(c["L"], c["n"], c["p"], c["g_cible"], c["comptes"]["R"]) for c in cas] != [
            (L, n, p, g, R0 // dv) for L, n, p, g, R0 in TABLE] or J["parametres"]["cas"] != [list(x) for x in TABLE]:
        echec("T0", "cas de la sortie différents de la table du pré-enregistrement")
    for c in cas:
        P = GO.pmore(c["p"])
        g = c["n"] * P * (1 - P)
        if not (c["g_cible"] <= g < Fraction(1001, 1000) * c["g_cible"] and c["g_theorique"] == float(g)):
            echec("T0", f"g théorique {float(g)}, L={c['L']} n={c['n']} p={c['p']}")
    n1 = sum(GO.invariants(c, c["comptes"]["R"]) for c in cas)
    n4b = O.invariants(a.json)[1] + sum(O.invariants(f)[1] for f in a.p1)
    e2, n4 = Fraction(0), 0
    for c in cas:
        P, ref = GO.pmore(c["p"]), c["reference_iid_P_connu"]
        m, v, k = c["n"] * P, c["n"] * P * (1 - P), math.ceil(c["n"] * P)
        while (k - m) ** 2 < Fraction(233, 100) ** 2 * v:
            k += 1
        with localcontext(GO.contexte()):
            Pd = Decimal(P.numerator) / Decimal(P.denominator)
        e2 = max(e2, GO.ecart_rel(r1.binomial_tail_ge(k, c["n"], Pd), Decimal(ref["niveau"])))
        if ref["k_etoile"] != k or e2 > GO.TOL or Decimal(ref["P_more"]) != Pd:
            echec("T2", f"k* {ref['k_etoile']} contre {k}, ou niveau, L={c['L']} n={c['n']} p={c['p']}")
        k4, V = c["comptes"], list(GO.CAS_R1.values())
        if c["n"] < 30 * ELL:
            if not (k4[V[0]] == 0 and k4[V[2]] == 0 and k4["z_bloc non publiée"] == k4["R"]
                    and k4[V[4]] == k4["z ≥ 2,33"] and c.get("deduction_etape_S") is True):
                echec("T4", f"déduction de l'étape S §1.2 non tenue, L={c['L']} n={c['n']} p={c['p']}")
            n4 += 1
    taches = []
    for c in cas:
        att = {r: GO.CAS_R1[cle] for cle, liste in (("rejette", "REJETTE"), ("discordance", "discordance_50_premieres"),
                                                     ("rejet_non_qualifiable", "rejet_non_qualifiable"))
               for r in c["indices"][liste]}
        taches += [(float(c["p"]), c["L"], c["n"], r, att.get(r))
                   for r in sorted(set(range(min(50, c["comptes"]["R"]))) | set(att))]
    for f in a.p1:
        P1 = json.loads(open(f, "rb").read().decode("utf-8"))
        taches += [(float(P1["parametres"]["p"]), c["L"], c["n"], r, None) for c in P1["cas"]
                   for r in range(min(10, c["comptes"]["R"]))]
    with multiprocessing.get_context("fork").Pool(a.processus) as pool:
        res = pool.map(GO.verifier, taches, 4)
    for x in res:
        if isinstance(x, str):
            sys.exit(x)
    emax = {k: str(float(max(ec[k] for ec, _ in res))) for k in ("P_more", "garde", "z", "z_bloc")}
    b = open(r1.__file__, "rb").read()
    sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
    rec = {"oracle": "SHOGEN-GARDE-NIVEAU-N-1 : table du pré-enregistrement, invariants, référence, déduction (T4), r1",
           "commit_r1": a.commit, "blob_r1": hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest(),
           "sha256_r1": hashlib.sha256(b).hexdigest(), "json": {os.path.basename(a.json): sha(a.json)},
           "p1": {f: sha(f) for f in a.p1},
           "script_sha256": {os.path.basename(f): sha(f) for f in (os.path.abspath(__file__), GO.__file__, O.__file__)},
           "T0_cas": len(cas), "T1_invariants": n1, "T1_invariants_4b_ii": n4b, "T2_ecart_relatif_max": str(float(e2)),
           "T3_replications": len(res), "T3_P_more_egaux_a_l_identique": sum(eg for _, eg in res),
           "T3_ecart_relatif_max": emax, "T4_cas": n4, "tolerance_relative": "1e-40"}
    with open(a.sortie, "xb") as f:
        f.write((json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
