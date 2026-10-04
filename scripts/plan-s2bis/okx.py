"""OKX (G0 du lot PLAN-S2BIS, sortie 3 ; SHOGEN-R1-HOTE-STRUCTUREL-1 ; ADR-0029 §1.2 pt 5) : mesure descriptive de la
contribution de la paire de flux OKX (okx_ticker, okx_index, lus sur le même hôte www.okx.com) à K de S2.

Sur le classement du rendu (pool S2, D1 ; σ et τ committés de S2 ; K, écarts par flux contrôlés égaux à la sortie
« base » de r1.compute_r1, sinon refus) : fenêtres à co-écart des deux flux, dans K et hors K ; types du co-écart ; co-écart
en panne_transport des deux flux ; K si la paire compte pour une seule unité (écart si l'un des deux flux l'est : la
fenêtre K ne reste que si m ≥ 3) ; K sans okx_index, sans okx_ticker (classement inchangé, colonne retirée) ; K sur le
pool D1-bis (médiane leave-one-out recalculée, retraits D1-bis). Comptes seulement : aucune statistique de test."""
from __future__ import annotations

from collections import Counter
from decimal import Decimal, localcontext

import commun

ITEMS = "contribution de la paire OKX à K de S2 (SHOGEN-R1-HOTE-STRUCTUREL-1)"
CLES = ("n", "K", "paire", "K_paire", "K_paire_pt", "perte_hote", "perte_index", "perte_ticker", "ecarts_tk", "ecarts_ix")


def comptes(fenetres: list, tk: str, ix: str, rmap: dict) -> dict:
    """Comptes d'une strate sur [(ws, {flux : Ecart}, prix)] ; un flux absent du classement n'est jamais en écart.
    perte_* : fenêtres K qui tombent sous deux écarts quand la paire fusionne ou qu'un flux est retiré (m = 2)."""
    r1 = commun.H["r1"]
    c, types = Counter(), Counter()
    for ws, cls, _rep in fenetres:
        e = {f for f, x in cls.items() if x in r1.ECARTS}
        m, a, b = len(e), tk in e, ix in e
        c.update(n=1, K=m >= 2, paire=a and b, ecarts_tk=a, ecarts_ix=b, perte_hote=a and b and m == 2,
                 perte_index=b and m == 2, perte_ticker=a and m == 2)
        if m >= 2 and a and b:
            types[cls[tk].value, cls[ix].value] += 1
            c.update(K_paire=1, K_paire_pt=all(rmap.get((ws, f), {}).get("status") == r1.PANNE_TRANSPORT for f in (tk, ix)))
    out = {k: int(c[k]) for k in CLES}
    out["types"] = types
    return out


def analyse(d: dict, prm: dict) -> list:
    r1, dec = commun.H["r1"], commun.dec
    tk, ix = prm["okx"]["flux"]
    par_s2, par_bis = commun.classer(d, d["pools_s2"]), commun.classer(d, d["pools_bis"])
    lignes = [f"[OKX] contribution de la paire de flux ({tk}, {ix} ; même hôte) à K de S2 ; descriptif, comptes de fenêtres "
              "(SHOGEN-R1-HOTE-STRUCTUREL-1)"]
    for st in prm["strates"]:
        if st not in par_s2:
            lignes.append(f"« {st} » : aucune fenêtre retenue dans la strate")
            continue
        c, b = comptes(par_s2[st], tk, ix, d["rmap"]), d["base"]["strates"][st]
        ps = b["per_source"]
        attendu = (b["K"], ps.get(tk, {}).get("ecart", 0), ps.get(ix, {}).get("ecart", 0))
        if (c["K"], c["ecarts_tk"], c["ecarts_ix"]) != attendu:
            raise ValueError(f"« {st} » : K ou écarts OKX recomptés différents de compute_r1 — fail-closed")
        absents = [f for f in (tk, ix) if f not in d["pools_s2"][st]]
        with localcontext(r1.contexte_decimal()):
            frac = dec(+(Decimal(c["perte_hote"]) / Decimal(c["K"]))) if c["K"] else "-"
        k_bis = sum(sum(x in r1.ECARTS for x in cls.values()) >= 2 for _ws, cls, _rep in par_bis.get(st, []))
        lignes += [f"« {st} » : n = {c['n']} ; K (pool S2 du rendu) = {c['K']} ; écarts : {tk} {c['ecarts_tk']}, {ix} "
                   f"{c['ecarts_ix']} fenêtres ; co-écart des deux flux : {c['paire']} fenêtres, dont {c['K_paire']} dans K"
                   + (f" ; absent(s) du pool S2 de la strate : {', '.join(absents)}" if absents else ""),
                   f"  dans K, types du co-écart ({tk}, {ix}) : "
                   + (" ; ".join(f"({x}, {y}) {k}" for (x, y), k in sorted(c["types"].items())) or "aucun"),
                   f"  dans K, les deux flux en panne_transport : {c['K_paire_pt']}",
                   f"  K si la paire compte pour une unité (écart si l'un des deux flux l'est) = {c['K'] - c['perte_hote']} "
                   f"(contribution de la paire : {c['perte_hote']} fenêtres, fraction de K {frac})",
                   f"  K sans {ix} (classement inchangé) = {c['K'] - c['perte_index']} ; K sans {tk} = "
                   f"{c['K'] - c['perte_ticker']}",
                   f"  K sur le pool D1-bis (médiane leave-one-out et retraits D1-bis appliqués) = {k_bis} (n = "
                   f"{len(par_bis.get(st, []))})"]
    return lignes


def main(argv=None) -> int:
    return commun.executer("okx", ITEMS, analyse, argv)


if __name__ == "__main__":
    raise SystemExit(main())
