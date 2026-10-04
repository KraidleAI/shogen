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
fenêtres sautées imputées avec les N flux en écart (c = s) ; borne « serrée » si les deux sont égales."""
from __future__ import annotations

from decimal import Decimal, localcontext
from itertools import combinations
from math import gcd

from commun import r1


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
