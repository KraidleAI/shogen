"""SHOGEN-CENSURE-INFO-2 (ADR-0028 annexe B.6 l.102 ; annexe D.5) : bornes extérieures de z_s sous censure arbitraire
des fenêtres sautées, J28, plage exclue, hors décision. Attribution « de type Manski » [inféré : P-08 non versée].

Modèle : chaque fenêtre sautée de la strate reçoit un vecteur quelconque de statuts des N flux du pool D1 ; n' = n + s,
e'_i = e_i + a_i, K' = K + c (c fenêtres imputées à au moins deux écarts). Imputations réalisables : 0 ≤ c ≤ s,
0 ≤ a_i ≤ s, Σ_i min(a_i, c) ≥ 2c, Σ_i (a_i − c)⁺ ≤ s − c. z' = (K' − n'·P)/√(n'·P(1 − P)), P = P_more de e'/n' en
rationnels exacts (entiers), Decimal 50 à la fin.
(i) Maximum : à K' fixé, z' décroît en P ; P croît en chaque a_i et est concave le long de tout transfert a_i → a_j tant
que Σ_k p_k/(1 − p_k) ≤ 1, ce qu'assure Σ_k e_k + 3c + max_k e_k ≤ n' (contrôlé pour chaque c) : le minimum de P sur
{0 ≤ a ≤ c, Σ a = 2c} est un sommet « deux flux à c ». Sinon, borne relâchée P ≥ P(e/n') pour ce c (c marqué).
(ii) Minimum : borne extérieure min_c f_c(P(e + c) + (s − c)/n') (∂P/∂a_i ≤ 1/n'), et témoin atteint : toutes les
fenêtres sautées imputées avec les N flux en écart (c = s) ; borne « serrée » si les deux sont égales.
(iii) Valeur de la règle (r1.regle_critere, z_bloc sur la série complétée aux positions sautées) sous deux imputations
témoins : W_A toutes propres ; W_B le plus petit c ≥ 1 qui donne REJETTE, c positions sautées imputées à deux écarts sur
la paire qui minimise P à ce c, toutes les ⌊s/c⌋ positions à partir de la première, les autres propres. Lecture « non
identifié sous censure arbitraire » si les deux valeurs diffèrent ; aucune borne extérieure de z_bloc n'est construite,
donc jamais « identifié » par cette construction."""
from __future__ import annotations

import sys
from decimal import Decimal, localcontext
from itertools import combinations
from math import gcd

import commun
from commun import dec, r1, records, window


def p_more(e: list, n: int) -> tuple:
    """(M, D) entiers : P_more = M/D pour p_i = e_i/n (identité élémentaire de doc 10 §5.1)."""
    q, pre, suf = [n - x for x in e], [1], [1]
    for x in q:
        pre.append(pre[-1] * x)
    for x in reversed(q):
        suf.append(suf[-1] * x)
    suf.reverse()
    d = n ** len(e)
    return d - pre[-1] - sum(x * pre[i] * suf[i + 1] for i, x in enumerate(e)), d


def z_de(k: int, n: int, num: int, den: int) -> Decimal:
    """(k − n·P)/√(n·P(1 − P)) pour P = num/den, 0 < P < 1 : (k·den − n·num)/√(n·num·(den − num)), Decimal 50, sur la
    fraction réduite (une même P rend la même valeur, quelle que soit sa représentation entière)."""
    g = gcd(num, den)
    num, den = num // g, den // g
    with localcontext(r1.contexte_decimal()):
        return +(Decimal(k * den - n * num) / Decimal(n * num * (den - num)).sqrt())


def bornes(n: int, k: int, e: list, s: int) -> dict:
    """Bornes de z_s sur toutes les imputations de s fenêtres sautées : max (exact hors c relâchés) et son sommet,
    borne inférieure extérieure, témoin « tout en écart », c relâchés."""
    n2, somme, plus = n + s, sum(e), max(e)
    m0, d = p_more(e, n2)
    best, arg, relachees = None, None, []
    for c in range(s + 1):
        if c and somme + 3 * c + plus > n2:
            relachees.append(c)
            num, paire = m0, None
        else:
            num, paire = min((p_more([x + c * (i in ij) for i, x in enumerate(e)], n2)[0], ij)
                             for ij in combinations(range(len(e)), 2)) if c else (m0, ())
        if 0 < num < d and (best is None or z_de(k + c, n2, num, d) > best):
            best, arg = z_de(k + c, n2, num, d), (c, paire)
    inf = None
    for c in range(s + 1):
        num, den = p_more([x + c for x in e], n2)[0] * n2 + (s - c) * d, d * n2
        z = Decimal("-Infinity") if num >= den else z_de(k + c, n2, num, den)
        inf = z if inf is None or z < inf else inf
    temoin = z_de(k + s, n2, p_more([x + s for x in e], n2)[0], d)
    return {"max": best, "argmax": arg, "relachees": relachees, "borne_inf": inf, "temoin_min": temoin,
            "serree": inf == temoin}


def strates(d: dict) -> dict:
    """Par strate du J28 : n, K, écarts e du pool D1, s (r1.fenetres_sautees, comme le rendu), positions sautées
    recomptées sur la grille, série I_t observée (r1.classify_cells) et ses contrôles."""
    spec, w, tous = d["params"]["strate_calendar"], d["w"], r1.build_window_strate(d["tous"])
    plages = records.exclusion_ranges(d["plages"])
    s, (t0, t1), pos = r1.fenetres_sautees(tous, spec, w, d["seg"], plages), d["seg"], {}
    for t in range(-(-t0 // w) * w, t1, w):
        if t not in tous and not any(a <= t <= b for a, b in plages):
            pos.setdefault(window.strate_from_spec(t, spec), []).append(t)
    out = {}
    for st, b in d["base"]["strates"].items():
        m, pool = [x for x in d["markers"] if x["strate"] == st], d["pools"][st]
        cls = r1.classify_cells(m, d["readings"], pool, w, d["sbc"], d["scf"], d["tau"], d["n_min"])
        serie = [(ws, int(sum(cls[ws, f] in r1.ECARTS for f in pool) >= 2)) for ws in sorted(r1.build_window_strate(m))]
        out[st] = {"n": b["n"], "K": b["K"], "e": [b["per_source"][f]["ecart"] for f in pool], "pool": pool,
                   "s": s.get(st, 0), "pos": pos.get(st, []), "serie": serie,
                   "controle": (len(pos.get(st, [])) == s.get(st, 0) and sum(i for _w, i in serie) == b["K"] and
                                r1.block_long_run_variance(serie, w)["sigma2_bloc"] == b["bloc"]["sigma2_bloc"])}
    return out


def temoin(x: dict, imput: dict, w: int, seuil) -> dict:
    """La règle scellée sur la strate complétée, calculée comme r1.compute_r1 puis r1.regle_critere : imput = {position
    sautée : indices des flux du pool en écart} (absente : propre)."""
    n2 = x["n"] + x["s"]
    e2 = [v + sum(i in imput.get(p, ()) for p in x["pos"]) for i, v in enumerate(x["e"])]
    k2 = x["K"] + sum(len(imput.get(p, ())) >= 2 for p in x["pos"])
    serie = sorted(x["serie"] + [(p, int(len(imput.get(p, ())) >= 2)) for p in x["pos"]])
    with localcontext(r1.contexte_decimal()):
        pm = r1.poisson_binomial([+(Decimal(v) / Decimal(n2)) for v in e2])[2]
    g = r1.gate_value(n2, pm)
    z = None if g < seuil else r1.z_score(n2, k2, pm)
    st = {"n": n2, "K": k2, "z": z, "gate_value": g, "bloc": r1.bloc_strate(serie, w, pm, g)}
    v = r1.regle_critere({"strates": {"s": st}})["strates"]["s"]
    return {**st, "P_more": pm, "z_bloc": st["bloc"]["z_bloc"], "valeur": v["valeur"], "cas": v["cas"]}


def recherche_rejette(x: dict, w: int, seuil):
    """(c, paire, témoin) du plus petit c ≥ 1 qui donne REJETTE dans la famille W_B ; None si aucun c ≤ s."""
    n2 = x["n"] + x["s"]
    for c in range(1, x["s"] + 1):
        paire = min(combinations(range(len(x["e"])), 2),
                    key=lambda ij: p_more([v + c * (i in ij) for i, v in enumerate(x["e"])], n2)[0])
        t = temoin(x, {p: paire for p in x["pos"][::x["s"] // c][:c]}, w, seuil)
        if t["valeur"] == "REJETTE":
            return c, paire, t
    return None


def _t(t: dict) -> str:
    return (f"n' = {t['n']} ; K' = {t['K']} ; P̂_more = {dec(t['P_more'])} ; garde = {dec(t['gate_value'])} ; z_s = "
            f"{dec(t['z'])} ; z_bloc = {dec(t['z_bloc'])} ; valeur = {t['valeur']} ({t['cas']})")


def identification(d: dict) -> dict:
    """Bornes de z_s, témoins W_A et W_B par strate, « R1 discrimine » sous chaque imputation témoin, lecture."""
    xs, w, seuil, wa, wb = strates(d), d["w"], d["seuil"], {}, {}
    lignes = ["[SHOGEN-CENSURE-INFO-2] chaque fenêtre sautée reçoit un vecteur quelconque de statuts des flux du pool "
              "D1 (bornes de type Manski [inféré : P-08 non versée]) ; H_perte n'est pas supposée ici"]
    for st, x in xs.items():
        lignes.append(f"« {st} » : n = {x['n']} ; K = {x['K']} ; N = {len(x['pool'])} flux ; s = {x['s']} ; positions "
                      f"sautées recomptées {len(x['pos'])} ; contrôles (positions, ΣI_t = K, σ̂²_bloc du rendu) : "
                      f"{'égaux' if x['controle'] else 'ÉCART, strate non traitée (fail-closed)'}")
        if not x["controle"]:
            continue
        b = bornes(x["n"], x["K"], x["e"], x["s"])
        c, ij = b["argmax"] or (None, None)
        rel = b["relachees"]
        lignes.append(f"« {st} » : z_s sur toutes les imputations : maximum = {dec(b['max'])} (c = {c}, flux en écart "
                      f"{[x['pool'][i] for i in ij or ()]}) " + (f"— borne relâchée pour {len(rel)} valeur(s) de c, de "
                      f"{rel[0]} à {rel[-1]}" if rel else "(exact)") + f" ; borne inférieure extérieure = "
                      f"{dec(b['borne_inf'])} ; témoin « tout en écart » (c = s) = {dec(b['temoin_min'])} (borne "
                      f"{'serrée' if b['serree'] else 'non serrée'})")
        wa[st] = temoin(x, {}, w, seuil)
        lignes.append(f"« {st} » : témoin W_A (toutes propres) : {_t(wa[st])}")
        if r := recherche_rejette(x, w, seuil):
            wb[st] = r
            lignes.append(f"« {st} » : témoin W_B (c = {r[0]} positions sautées, une toutes les {x['s'] // r[0]}, en "
                          f"écart sur {[x['pool'][i] for i in r[1]]}) : {_t(r[2])}")
        else:
            lignes.append(f"« {st} » : témoin W_B : aucun c ≤ s ne donne REJETTE dans cette famille")
    agg, non = (lambda s: r1.regle_critere({"strates": s})["r1_discrimine"]), []
    lignes.append("« R1 discrimine » sous W_A (imputation témoin ; hors décision ; ne change pas le verdict) = "
                  f"{agg(wa)}")
    for st, (_c, _ij, t) in wb.items():
        non += [st] if agg({**wa, st: t}) != agg(wa) else []
        lignes.append(f"« R1 discrimine » sous W_B dans « {st} », W_A ailleurs (imputation témoin ; hors décision ; ne "
                      f"change pas le verdict) = {agg({**wa, st: t})}")
    lecture = "non identifié sous censure arbitraire" if non else "identification non établie par cette construction"
    lignes.append(f"lecture : {lecture} ; aucune borne extérieure de z_bloc n'est construite, donc aucune lecture "
                  "« identifié » par cette construction")
    return {"strates": xs, "wa": wa, "wb": wb, "lecture": lecture, "lignes": lignes}


def main(argv: list) -> int:
    return commun.executer("censure.py", "SHOGEN-CENSURE-INFO-2", lambda d: identification(d)["lignes"], argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
