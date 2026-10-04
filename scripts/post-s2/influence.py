"""SHOGEN-DEP-FENETRES-2 (b), qui est aussi SHOGEN-R1-PLUGIN-1 (a), SHOGEN-DEP-FENETRES-2 (c) et SHOGEN-R1-PLUGIN-1 (b)
descriptif (ADR-0028 annexe B.6 l.98-99), J28, plage exclue, hors décision, exploratoires.

(b) Variance de la fonction d'influence de K/n − P_more(p̂), fonction lisse de moyennes (Künsch 1989, Ex. 2.2 p. 1219 ;
estimateur (2.14) p. 1222, poids de Bartlett 1 − |k|/ℓ, ℓ = r1.ELL_BLOC, lag sur la grille, série complétée par des 0) :
IF_t = (I_t − Ī) − Σ_i g_i (D_it − p̂_i), g_i = ∂P_more/∂p_i(p̂) = Σ_{j≠i} p̂_j Π_{k∉{i,j}} (1 − p̂_k) ; entiers
J_t = n^N·IF_t, Decimal 50 à la fin ; z_IF = (K − n·P̂_more)/σ̂_IF, P̂_more en rationnel exact.
(c) Runs de I_t pris comme unités, tolérance 0 (définition de r1.bloc_strate) : R, E[R] et Var[R] exacts sous fenêtres iid
de probabilité P̂_more (plug-in), z_R = (R − E[R])/√Var[R].
R1-PLUGIN-1 (b) : comptes observés de m_t = Σ_i D_it contre n·PB(m ; p̂), descriptifs, sans test ni p-valeur.
(a) fixed-b (Kiefer & Vogelsang 2005, P-05) : non faite, source non détenue."""
from __future__ import annotations

import sys
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from math import prod

import commun
from commun import dec, r1


def _blocs(valeurs: dict, ell: int) -> int:
    """Σ_j B_j², B_j somme des valeurs (position de grille → entier) sur [j ; j + ℓ − 1], série complétée par des 0."""
    pre, fin = [0], max(valeurs) + 1
    for t in range(fin):
        pre.append(pre[-1] + valeurs.get(t, 0))
    return sum((pre[min(j + ell, fin)] - pre[max(j, 0)]) ** 2 for j in range(1 - ell, fin))


def _d(x: Fraction) -> Decimal:
    with localcontext(r1.contexte_decimal()):
        return Decimal(x.numerator) / Decimal(x.denominator)


def influence(serie: list, w: int, ell: int) -> dict:
    """serie : [(window_start, (D_1t, …, D_Nt))] triée, une strate."""
    n, nf = len(serie), len(serie[0][1])
    e, it = [sum(v[i] for _w, v in serie) for i in range(nf)], [int(sum(v) >= 2) for _w, v in serie]
    k, q, dd = sum(it), [n - x for x in e], n ** nf
    g = [sum(e[j] * prod(q[m] for m in range(nf) if m not in (i, j)) for j in range(nf) if j != i) for i in range(nf)]
    num = k * dd - n * (dd - prod(q) - sum(e[i] * prod(q[:i] + q[i + 1:]) for i in range(nf)))
    jt = [n ** (nf - 1) * (n * i_t - k) - sum(g[i] * (n * v[i] - e[i]) for i in range(nf)) for (_w, v), i_t in
          zip(serie, it)]
    s0, sb = sum(x * x for x in jt), _blocs({(ws - serie[0][0]) // w: x for (ws, _v), x in zip(serie, jt)}, ell)
    with localcontext(r1.contexte_decimal()):
        z0 = +(Decimal(num) / Decimal(s0).sqrt()) if s0 else None
        zb = +(Decimal(num) * Decimal(ell).sqrt() / Decimal(sb).sqrt()) if sb else None
    return {"n": n, "K": k, "numerateur": Fraction(num, dd), "s0": Fraction(s0, dd * dd),
            "sbloc": Fraction(sb, ell * dd * dd), "z0": z0, "zbloc": zb}


def runs(serie: list, w: int, p) -> dict:
    """serie : [(window_start, I_t)] triée ; p : P̂_more. μ_t = p sans prédécesseur présent, p(1 − p) sinon ;
    Cov(X_t, X_t+1) = −μ_t·μ_t+1 pour deux fenêtres voisines présentes, 0 au-delà."""
    p, val = Fraction(p), dict(serie)
    m0, m1 = p, p * (1 - p)
    h = {ws: (ws - w) in val for ws in val}
    r = sum(i and not (h[ws] and val[ws - w]) for ws, i in serie)
    n1, a = sum(h.values()), sum(h[ws] and h[ws - w] for ws in val)
    e = (len(serie) - n1) * m0 + n1 * m1
    v = (len(serie) - n1) * m0 * (1 - m0) + n1 * m1 * (1 - m1) - 2 * (a * m1 * m1 + (n1 - a) * m0 * m1)
    longueurs, c, avant = Counter(), 0, None
    for ws, i in serie:
        c = (c + 1 if avant == ws - w else 1) if i else 0
        longueurs[c] += bool(i)
        longueurs[c - 1] -= bool(i) and c > 1
        avant = ws
    with localcontext(r1.contexte_decimal()):
        z = +((_d(Fraction(r) - e)) / _d(v).sqrt())
    return {"R": r, "E": e, "V": v, "z": z, "longueurs": {k: x for k, x in sorted(longueurs.items()) if x}}


def loi_m(serie: list) -> dict:
    """Comptes observés de m_t = Σ_i D_it et n·PB(m ; p̂), p̂_i = e_i/n exacts."""
    n, nf = len(serie), len(serie[0][1])
    obs, coef = Counter(sum(v) for _w, v in serie), [Fraction(1)]
    for i in range(nf):
        p = Fraction(sum(v[i] for _w, v in serie), n)
        coef = [(coef[m] if m < len(coef) else 0) * (1 - p) + (coef[m - 1] * p if m else 0) for m in range(len(coef) + 1)]
    return {"observes": [obs[m] for m in range(nf + 1)], "attendus": [n * c for c in coef]}


def analyse(d: dict) -> dict:
    """Par strate : cellules de r1.classify_cells (pool D1 de la strate), puis (b), (c) et la loi de m_t ; lignes."""
    res, lignes = {"strates": {}}, [
        "[SHOGEN-DEP-FENETRES-2 (b) = SHOGEN-R1-PLUGIN-1 (a)] variance de la fonction d'influence (Künsch 1989, (2.14) "
        "p. 1222, Ex. 2.2 p. 1219) : IF_t = (I_t − Ī) − Σ_i g_i (D_it − p̂_i), g_i = ∂P_more/∂p_i ; Bartlett, ℓ = "
        f"{r1.ELL_BLOC}, grille ; σ̂² à l'échelle des sommes (celle de σ̂²_bloc) ; exploratoire"]
    for st, b in d["base"]["strates"].items():
        m, pool = [x for x in d["markers"] if x["strate"] == st], d["pools"][st]
        cls = r1.classify_cells(m, d["readings"], pool, d["w"], d["sbc"], d["scf"], d["tau"], d["n_min"])
        serie = [(ws, tuple(int(cls[ws, f] in r1.ECARTS) for f in pool)) for ws in sorted(r1.build_window_strate(m))]
        x = res["strates"][st] = {"inf": influence(serie, d["w"], r1.ELL_BLOC), "loi": loi_m(serie),
                                  "runs": runs([(ws, int(sum(v) >= 2)) for ws, v in serie], d["w"], b["P_more"])}
        i = x["inf"]
        with localcontext(r1.contexte_decimal()):
            r0, rb = _d(i["s0"]) / b["gate_value"], _d(i["sbloc"]) / b["bloc"]["sigma2_bloc"]
        lignes.append(f"« {st} » : K − n·P̂_more = {dec(_d(i['numerateur']))} ; Σ IF² = {dec(_d(i['s0']))} (rapport à "
                      f"n·P̂(1 − P̂) : {dec(r0)}) ; σ̂²_IF,bloc = {dec(_d(i['sbloc']))} (rapport à σ̂²_bloc : "
                      f"{dec(rb)}) ; z_IF,0 = {dec(i['z0'])} ; z_IF,bloc = {dec(i['zbloc'])}")
    lignes.append("[SHOGEN-DEP-FENETRES-2 (c)] runs de I_t pris comme unités, tolérance 0 (définition de r1.bloc_strate) ;"
                  " loi nulle : fenêtres iid de probabilité P̂_more (plug-in), sans persistance propre des sources ; "
                  "exploratoire")
    for st, x in res["strates"].items():
        u = x["runs"]
        lignes.append(f"« {st} » : R = {u['R']} (runs de r1 : {d['base']['strates'][st]['bloc']['runs']['nombre']}) ; "
                      f"E[R] = {dec(_d(u['E']))} ; Var[R] = {dec(_d(u['V']))} ; z_R = {dec(u['z'])} ; longueurs : "
                      f"{u['longueurs']}")
    lignes += ["[SHOGEN-DEP-FENETRES-2 (a)] fixed-b (Kiefer & Vogelsang 2005, P-05) : non faite, source non détenue",
               "[SHOGEN-R1-PLUGIN-1 (b), descriptif] comptes de m_t (écarts par fenêtre) contre n·PB(m ; p̂) exacts ; "
               "aucun test, aucune p-valeur (statistique et niveau à sourcer)"]
    for st, x in res["strates"].items():
        lignes += [f"« {st} » : m = {m} : observé {o} ; attendu {dec(_d(a))}"
                   for m, (o, a) in enumerate(zip(x["loi"]["observes"], x["loi"]["attendus"]))]
    res["lignes"] = lignes
    return res


def main(argv: list) -> int:
    return commun.executer("influence.py", "SHOGEN-DEP-FENETRES-2 (b) et (c) ; SHOGEN-R1-PLUGIN-1 (a) et (b)",
                           lambda d: analyse(d)["lignes"], argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
