"""SHOGEN-SIGMA-BLOC-INDEP-1 (ADR-0028 annexe B.46 l.686) : σ̂²_bloc recalculé sur les journaux réels par un code
indépendant de r1, J28, plage exclue, hors décision. Indépendants de r1 : dernière lecture par (fenêtre, flux), pool D1,
classification (définition imprimée au bloc 3 du rendu : panne > staleness > hors-enveloppe ; σ et τ par classe ; au
moins n_min répondantes ; médiane leave-one-out > 0 ; comparaison exacte |p − m| > τ·m), série I_t = 1{m_t ≥ 2} et
variance Σ_j B_j²/(ℓ·n²), B_j sommes de blocs de longueur ℓ de c_t = n·I_t − K sur la grille de pas w complétée par des
0. Lecteurs communs : r1.parse_journal et le filtre de lecture (commun.charger). Comparaisons : classification cellule par
cellule contre r1.classify_cells, écarts par flux et σ̂²_bloc contre r1, γ̂₀ et σ̂²_bloc contre le bloc 3 du rendu."""
from __future__ import annotations

import re
import sys
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext

import commun
from commun import dec, r1


def variance(serie: list, w: int, ell: int) -> dict:
    """n, K, γ̂₀ = K(n − K)/n et σ̂² = Σ_j B_j²/(ℓ·n²) d'une série (window_start, I_t) triée."""
    n, k = len(serie), sum(i for _w, i in serie)
    if not n:
        return {"n": 0, "K": 0, "gamma0": None, "sigma2": None}
    c = {(ws - serie[0][0]) // w: n * i - k for ws, i in serie}
    pre, fin = [0], max(c) + 1
    for t in range(fin):
        pre.append(pre[-1] + c.get(t, 0))
    tot = sum((pre[min(j + ell, fin)] - pre[max(j, 0)]) ** 2 for j in range(1 - ell, fin))
    with localcontext(Context(prec=50, rounding=ROUND_HALF_EVEN)):
        return {"n": n, "K": k, "gamma0": Decimal(n * k - k * k) / Decimal(n),
                "sigma2": Decimal(tot) / Decimal(ell * n * n)}


def ecart(r, f, rep, fin, sigma, tau, n_min) -> int:
    """1 si panne, staleness ou hors-enveloppe ; 0 sinon (non évaluable compris)."""
    if r is None or r.get("status") != "ok" or r.get("price") is None:
        return 1
    if sigma is not None and r.get("source_ts") is not None and Decimal(fin) - Decimal(str(r["source_ts"])) > sigma:
        return 1
    if len(rep) < n_min or tau is None:
        return 0
    a = sorted(v for g, v in rep.items() if g != f)
    m = a[len(a) // 2] if len(a) % 2 else (a[len(a) // 2 - 1] + a[len(a) // 2]) / 2
    return int(m > 0 and abs(rep[f] - m) > tau * m)


def classer(d: dict) -> tuple:
    """({strate : {(ws, f) : écart}}, pools D1) sur les fenêtres retenues."""
    p, der, strate = d["params"], {}, {}
    sig = {k: None if v is None else Decimal(str(v)) for k, v in p["sigma_classe"].items()}
    tau, cl = {k: Decimal(str(v)) for k, v in p["tau_classe"].items()}, p["sigma_class_of_flux"]
    for r in d["readings"]:
        der[int(r["window_start"]), r["flux_id"]] = r
    for m in d["markers"]:
        strate[int(m["window_start"])] = m["strate"]
    ok = lambda r: r is not None and r.get("status") == "ok" and r.get("price") is not None
    pools = {st: [f for f in p["pool"] if any(ok(der.get((ws, f))) for ws, s in strate.items() if s == st)]
             for st in sorted(set(strate.values()))}
    out = {st: {} for st in pools}
    with localcontext(Context(prec=50, rounding=ROUND_HALF_EVEN)):
        for ws, st in sorted(strate.items()):
            rep = {f: Decimal(der[ws, f]["price"]) for f in pools[st] if ok(der.get((ws, f)))}
            for f in pools[st]:
                out[st][ws, f] = ecart(der.get((ws, f)), f, rep, ws + d["w"], sig.get(cl.get(f)), tau.get(cl.get(f)),
                                       d["n_min"])
    return out, pools


def lire_rendu(chemin: str) -> dict:
    """{strate : (γ̂₀, σ̂²_bloc) en chaînes} lus au bloc 3 du rendu."""
    with open(chemin, encoding="utf-8") as f:
        b3 = f.read().split("\n[BLOC 3]", 1)[1].split("\n[BLOC 4]", 1)[0]
    return {m.group(1): (m.group(2), m.group(3)) for x in b3.split("\n") if (m := re.match(
        "    « (\\w+) » : ℓ = \\d+ ; γ̂₀ = (\\S+) ; σ̂\xb2_bloc = (\\S+) ; cv", x))}


def recalcul(d: dict, rendu=None) -> dict:
    mine, pools = classer(d)
    res, lus = {"strates": {}, "desaccords": {}, "ecarts": {}, "lignes": []}, lire_rendu(rendu) if rendu else {}
    res["lignes"].append("[SHOGEN-SIGMA-BLOC-INDEP-1] code indépendant de r1 (classification, série, variance Σ_j B_j²/"
                         f"(ℓ·n²), ℓ = {r1.ELL_BLOC}) ; pools D1 recomptés égaux à r1 : "
                         f"{'oui' if pools == {s: d['pools'].get(s) for s in pools} else 'non'}")
    for st, cells in mine.items():
        m = [x for x in d["markers"] if x["strate"] == st]
        ref = r1.classify_cells(m, d["readings"], d["pools"][st], d["w"], d["sbc"], d["scf"], d["tau"], d["n_min"])
        res["desaccords"][st] = sum(v != int(ref.get(c) in r1.ECARTS) for c, v in cells.items()) + len(
            set(ref) - set(cells))
        res["ecarts"][st] = {f: sum(v for (_w, g), v in cells.items() if g == f) for f in pools[st]}
        serie = [(ws, int(sum(cells[ws, f] for f in pools[st]) >= 2)) for ws in sorted({ws for ws, _f in cells})]
        v = res["strates"][st] = variance(serie, d["w"], r1.ELL_BLOC)
        b = d["base"]["strates"][st]
        egal_r1 = (v["n"], v["K"], v["sigma2"]) == (b["n"], b["K"], b["bloc"]["sigma2_bloc"])
        egal_ecarts = res["ecarts"][st] == {f: b["per_source"][f]["ecart"] for f in pools[st]}
        egal_rendu = lus.get(st) == (dec(v["gamma0"]), dec(v["sigma2"]))
        res["lignes"] += [f"« {st} » : cellules classées {len(cells)} ; désaccords avec r1.classify_cells "
                          f"{res['desaccords'][st]} ; écarts par flux égaux à r1 : {'oui' if egal_ecarts else 'non'}",
                          f"« {st} » : n = {v['n']} ; K = {v['K']} ; γ̂₀ = {dec(v['gamma0'])} ; σ̂²_bloc = "
                          f"{dec(v['sigma2'])} ; égaux à r1 : {'oui' if egal_r1 else 'non'}"
                          + (f" ; égaux au bloc 3 du rendu (γ̂₀, σ̂²_bloc) : {'oui' if egal_rendu else 'non'}"
                             if rendu else "")]
    return res


def main(argv: list) -> int:
    rendu = argv[argv.index("--rendu") + 1] if "--rendu" in argv else commun.RENDU_J28
    return commun.executer("sigma_indep.py", "SHOGEN-SIGMA-BLOC-INDEP-1", lambda d: recalcul(d, rendu)["lignes"], argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
