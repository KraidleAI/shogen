"""SHOGEN-SIM-NIVEAU-ORACLE4-1 : oracle (4) du G0 de SIM-NIVEAU (§8) contre r1.block_long_run_variance (lot B-DEP-1).
Pour les --replications premières réplications de chaque cas de sim_niveau.CAS (p = P_DEFAUT) : la série I_t est
régénérée par sim_niveau_oracle_r1.serie (texte du G0, sans sim_niveau_calc) ; r1.block_long_run_variance (export
`git archive <commit> s2-harness`, jamais F:/Shogen) doit rendre n, K et le numérateur entier N = ℓ·n²·σ̂² égaux à
ceux de sim_niveau_calc.replication, et σ̂²_bloc égal (== et str) à N / (ℓ·n²) en Decimal à r1.DECIMAL_PREC.
Sortie ≠ 0 au premier écart (« ECHEC (4) »), aucun fichier écrit ; sinon enregistrement JSON (mode xb).
Orchestrateur Shōgen claude-opus-5-5, 2026-10-01 (partie 1 de la fin de S2, docs/adr-0028/PARTIES-S2.md).
Usage : python -B sim_niveau_oracle4.py --r1 EXPORT/s2-harness --commit SHA --sortie FICHIER.json [--replications 10]"""
import argparse, hashlib, json, os, sys
from decimal import Decimal, localcontext


def main():
    ap = argparse.ArgumentParser(description="oracle (4) de SHOGEN-SIM-NIVEAU-1 contre r1.block_long_run_variance")
    ap.add_argument("--r1", required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--replications", type=int, default=10)
    a = ap.parse_args()
    if os.path.exists(a.sortie):
        sys.exit("refus : le fichier de sortie existe deja")
    sys.path.insert(0, os.path.abspath(a.r1))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import sim_niveau as S, sim_niveau_calc as C, sim_niveau_oracle_r1 as O
    from shogen_s2 import r1
    ell, w, cas, total = O.ELL, 60, [], 0
    for L, n in S.CAS:
        for r in range(a.replications):
            d = C.replication(S.P_DEFAUT, L, n, r)
            _e, _runs, I = O.serie(S.P_DEFAUT, L, n, r)
            out = r1.block_long_run_variance([(t * w, i) for t, i in enumerate(I)], w, ell=ell)
            with localcontext() as ctx:
                ctx.prec = r1.DECIMAL_PREC
                s2 = +(Decimal(d["N"]) / Decimal(ell * n * n))
            for nom, x, y in (("n", out["n"], n), ("K", out["K"], d["K"]), ("N", out["numerateur"], d["N"]),
                              ("sigma2_bloc", out["sigma2_bloc"], s2)):
                if not (x == y and str(x) == str(y)):
                    sys.exit(f"ECHEC (4) : {nom}, L={L} n={n} r={r} : r1 {str(x)[:60]}, script {str(y)[:60]}")
            total += 4
        cas.append({"L": L, "n": n, "replications": a.replications})
    b = open(r1.__file__, "rb").read()
    rec = {"oracle": "(4) SHOGEN-SIM-NIVEAU-ORACLE4-1 : r1.block_long_run_variance = sigma2 du script",
           "commit_r1": a.commit, "blob_r1": hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest(),
           "sha256_r1": hashlib.sha256(b).hexdigest(), "p": repr(S.P_DEFAUT), "ell": ell, "w": w,
           "comparaison": "entiers n, K, N : == ; sigma2_bloc Decimal : == et str()", "egalites_total": total, "cas": cas}
    with open(a.sortie, "xb") as f:
        f.write((json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
