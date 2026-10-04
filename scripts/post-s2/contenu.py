"""SHOGEN-CONTENU-DEP-1 (ADR-0028 annexe B.6 l.103 ; paquet §12 pt 12) : dépendance sérielle sur l'axe contenu, J28,
plage exclue, hors décision, exploratoire. Pour chaque paire du pool R2 (pool D1 du segment) et pour ρ_raw (log-rendements
de r2.log_returns aux fenêtres communes) et ρ_resid (résidus à la médiane leave-two-out des ln-prix, au moins 4 autres
répondantes, comme r2.rho_resid) : ρ̂ de r2.pearson ; ρ̂ est une fonction lisse de moyennes (Künsch 1989, Ex. 2.2
p. 1219), de fonction d'influence IF_t = x̃_t·ỹ_t/√(s_xx·s_yy) − (ρ̂/2)(x̃_t²/s_xx + ỹ_t²/s_yy), moments empiriques
[inféré : dérivée ici] ; Var̂_bloc(ρ̂) = Σ_j B_j(IF)²/(ℓ·N²) (estimateur (2.14) p. 1222, Bartlett, ℓ = r1.ELL_BLOC, lag
sur la grille, série complétée par des 0), Var̂_0(ρ̂) = Σ_t IF_t²/N² ; SE de Fisher (1 − ρ̂²)/√(N − 3) (paires
indépendantes) ; N_eff = 3 + (1 − ρ̂²)²/Var̂_bloc (le N pour lequel le SE de Fisher égale le SE par blocs), N_eff,0 avec
Var̂_0. Paire sous N_min = content_n_min fenêtres communes : non calculée, comme r2."""
from __future__ import annotations

import re
import sys
from decimal import Decimal, localcontext
from itertools import combinations

import commun
from commun import dec, r1
from shogen_s2 import r2


def dependance(serie: list, w: int, ell: int) -> dict:
    """serie : [(window_start, x, y)] triée, Decimal."""
    rho = r2.pearson([x for _w, x, _y in serie], [y for _w, _x, y in serie])[0]
    with localcontext(r1.contexte_decimal()):
        n = Decimal(len(serie))
        mx, my = sum(x for _w, x, _y in serie) / n, sum(y for _w, _x, y in serie) / n
        sxx = sum((x - mx) ** 2 for _w, x, _y in serie) / n
        syy = sum((y - my) ** 2 for _w, _x, y in serie) / n
        q = (sxx * syy).sqrt()
        inf = {(ws - serie[0][0]) // w: (x - mx) * (y - my) / q - rho / 2 * ((x - mx) ** 2 / sxx + (y - my) ** 2 / syy)
               for ws, x, y in serie}
        pre, fin = [Decimal(0)], max(inf) + 1
        for t in range(fin):
            pre.append(pre[-1] + inf.get(t, Decimal(0)))
        sb = sum((pre[min(j + ell, fin)] - pre[max(j, 0)]) ** 2 for j in range(1 - ell, fin))
        v0, vb, u = sum(v * v for v in inf.values()) / (n * n), sb / (ell * n * n), (1 - rho * rho) ** 2
        return {"N": len(serie), "rho": rho, "var0": +v0, "varbloc": +vb,
                "se_fisher": +((1 - rho * rho) / (n - 3).sqrt()) if n > 3 else None,
                "neff": +(3 + u / vb) if vb > 0 else None, "neff0": +(3 + u / v0) if v0 > 0 else None}


def series(d: dict):
    """((a, b), série ρ_raw, série ρ_resid) pour chaque paire du pool R2, mêmes fenêtres que r2.compute_content."""
    wins, rmap = r2.price_map(d["readings"], d["markers"])
    lnp = r2.lnprice_by_window(wins, rmap)
    ret = {f: r2.log_returns(wins, lnp, f, d["w"]) for f in d["pool"]}
    for a, b in combinations(d["pool"], 2):
        resid = []
        with localcontext(r1.contexte_decimal()):
            for ws in wins:
                c = lnp.get(ws, {})
                autres = [v for f, v in c.items() if f not in (a, b)] if a in c and b in c else []
                if len(autres) >= 4:
                    m = r1._median(autres)
                    resid.append((ws, +(c[a] - m), +(c[b] - m)))
        yield (a, b), [(ws, ret[a][ws], ret[b][ws]) for ws in sorted(set(ret[a]) & set(ret[b]))], resid


def lire_bloc5(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        b5 = f.read().split("\n[BLOC 5]", 1)[1].split("\n[BLOC 6]", 1)[0]
    return {(m.group(1), m.group(2)): (m.group(3), m.group(4)) for x in b5.split("\n")
            if (m := re.match("\\s+(\\S+)×(\\S+)\\s+ρ_raw=(\\S+) ρ_resid=(\\S+) \\|", x))}


def analyse(d: dict, n_min: int, rendu=None) -> dict:
    lus, paires, lignes = lire_bloc5(rendu) if rendu else {}, {}, [
        f"[SHOGEN-CONTENU-DEP-1] Var̂_bloc(ρ̂) par la fonction d'influence (Künsch 1989, Ex. 2.2, (2.14)), ℓ = "
        f"{r1.ELL_BLOC}, grille ; SE de Fisher (1 − ρ̂²)/√(N − 3) ; N_eff = 3 + (1 − ρ̂²)²/Var̂_bloc ; N_min = {n_min} ; "
        "SE et N_eff à 6 chiffres significatifs ; exploratoire"]
    g = lambda x: "-" if x is None else format(x, ".6g")
    for (a, b), raw, resid in series(d):
        x = paires[a, b] = {k: dependance(s, d["w"], r1.ELL_BLOC) if len(s) >= n_min else {"rho": None, "N": len(s)}
                            for k, s in (("raw", raw), ("resid", resid))}
        egal = lus.get((a, b)) == (dec(x["raw"]["rho"]), dec(x["resid"]["rho"]))
        lignes.append(f"{a}×{b} : " + " ; ".join(
            f"ρ_{k} N = {v['N']}, ρ̂ = {dec(v['rho'])}" + (f", SE_F = {g(v['se_fisher'])}, SE_bloc = "
                                                         f"{g(v['varbloc'].sqrt())}, N_eff = {g(v['neff'])}, N_eff,0 = "
                                                         f"{g(v['neff0'])}" if v["rho"] is not None else "")
            for k, v in x.items()) + (f" ; ρ̂ égaux au bloc 5 : {'oui' if egal else 'non'}" if rendu else ""))
    for k in ("raw", "resid"):
        v = sorted((x[k]["neff"] / x[k]["N"], x[k]["neff"]) for x in paires.values() if x[k].get("neff") is not None)
        lignes.append(f"ρ_{k} : paires calculées {len(v)} ; N_eff < N_min = {n_min} : {sum(e < n_min for _r, e in v)} ; "
                      f"N_eff/N min {g(v[0][0]) if v else '-'}, médiane {g(v[len(v) // 2][0]) if v else '-'}, max "
                      f"{g(v[-1][0]) if v else '-'}")
    return {"paires": paires, "lignes": lignes}


def main(argv: list) -> int:
    rendu = argv[argv.index("--rendu") + 1] if "--rendu" in argv else commun.RENDU_J28
    return commun.executer("contenu.py", "SHOGEN-CONTENU-DEP-1", lambda d: analyse(
        d, int(d["params"]["content_n_min"]), rendu)["lignes"], argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
