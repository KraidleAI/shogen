"""SHOGEN-FLUX-QUASI-MORT-1 (avec SHOGEN-QUASI-MORT-PREDICAT-1 et SHOGEN-POOL-MIN-1) et SHOGEN-FLUX-DEVIANT-1 (ADR-0028
annexe B.6 l.101, B.39, B.44) : sensibilités « pool réduit » de la règle scellée SHOGEN-CRITERE-R1-1, J28, plage exclue.

QUASI-MORT-1, seuil fixé d'avance (`docs/adr-0028/AVIS-SEUIL-FLUX-QUASI-MORT.md` §1) : f retiré du pool de la strate s si
2·ok(f, s) < n_s ; ok(f, s) = `ok_windows` de r1.compute_r1 (statut ok et prix non nul, lectures last-wins de la liste de
r1.parse_journal : le prédicat de r1.analysis_pools, PREDICAT-1), 0 pour un flux retiré par D1 ; égalité : le flux reste.
DEVIANT-1 (même avis, L2 et V2) : f retiré si 2·écart(f, s) > n_s (p̂_f > 1/2), écart de r1.compute_r1 sur le pool D1.
Une passe, par strate, sans itération ; POOL-MIN-1 : pool réduit de moins de r1.N_MIN_HORSENV flux, refus nommé, aucun z
pour la strate ni « R1 discrimine » recalculé. Règle : r1.compute_r1 sur les pools réduits, puis r1.regle_critere."""
from __future__ import annotations

import sys

import commun
from commun import dec, r1
from shogen_s2 import r2

QUASI_MORT = ("SHOGEN-FLUX-QUASI-MORT-1", "ok_windows", lambda v, n: 2 * v < n,
              "retrait de f si 2·ok(f, s) < n_s (ok_windows de r1.compute_r1 ; 0 si retiré par D1)", "")
DEVIANT = ("SHOGEN-FLUX-DEVIANT-1", "ecart", lambda v, n: 2 * v > n,
           "retrait de f si 2·écart(f, s) > n_s (p̂_f > 1/2 ; écart de r1.compute_r1 sur le pool D1)",
           " ; exploratoire, conditionnée sur une composante du résultat (p̂_f)")


def sensibilite(d: dict, crit: tuple) -> dict:
    """Pools réduits par strate selon `crit`, garde POOL-MIN-1, règle recalculée ; rend aussi les lignes de sortie."""
    item, cle, retire, texte, sup = crit
    pools, ok, egal, refus = {}, {}, [], []
    lignes = [f"[{item}] {texte} ; égalité : le flux reste ; une passe, par strate{sup}"]
    for st, b in sorted(d["base"]["strates"].items()):
        n, ps = b["n"], b["per_source"]
        ok[st] = {f: ps[f]["ok_windows"] if f in ps else 0 for f in d["params"]["pool"]}
        reste = [f for f in d["pools"][st] if not retire(ps[f][cle], n)]
        egal += [(st, f) for f in d["pools"][st] if 2 * ps[f][cle] == n]
        lignes.append(f"« {st} » : n_s = {n} ; " + " ; ".join(
            (f"{f} {cle} = {ps[f][cle]}" + ("" if f in reste else " (retiré)")) if f in ps else f"{f} retiré par D1"
            for f in d["params"]["pool"]))
        if len(reste) < r1.N_MIN_HORSENV:
            refus.append(st)
            lignes.append(f"« {st} » : refus nommé (SHOGEN-POOL-MIN-1) : pool réduit de {len(reste)} flux < "
                          f"N_MIN_HORSENV = {r1.N_MIN_HORSENV} ; aucun z calculé pour cette strate")
        else:
            pools[st] = reste
            lignes.append(f"« {st} » : pool réduit de {len(reste)} flux, k nominal_s = "
                          f"{len(r2.hosts_of_pool(d['params'].get('flux_hosts', {}), reste))} hôte(s) ; égalités : "
                          f"{[f for s, f in egal if s == st] or 'aucune'}")
    r = commun.calculer(d, [x for x in d["markers"] if x["strate"] in pools], pools)
    v = r1.regle_critere(r)
    for st, b in r["strates"].items():
        e = v["strates"][st]
        lignes.append(f"règle recalculée « {st} » : n = {b['n']} ; K = {b['K']} ; P̂_more = {dec(b['P_more'])} ; garde = "
                      f"{dec(b['gate_value'])} ; z_s = {dec(b['z'])} ; σ̂²_bloc = {dec(b['bloc']['sigma2_bloc'])} ; "
                      f"z_bloc = {dec(b['bloc']['z_bloc'])} ; valeur = {e['valeur']} ({e['cas']}) ; EMD_s = "
                      f"{dec(e['emd'])} ; sortie r1 égale à celle de la règle scellée : "
                      f"{'oui' if b == d['base']['strates'][st] else 'non'}")
    if not refus:
        lignes.append("« R1 discrimine » recalculé sous cette sensibilité (hors décision ; ne change pas le verdict) = "
                      f"{v['r1_discrimine']}")
    return {"pools": pools, "ok": ok, "egalites": egal, "refus": refus, "r1": r, "regle": v, "lignes": lignes}


ANALYSES = {"quasi-mort": ("SHOGEN-FLUX-QUASI-MORT-1 (+ QUASI-MORT-PREDICAT-1, POOL-MIN-1)",
                           lambda d: sensibilite(d, QUASI_MORT)["lignes"]),
            "deviant": ("SHOGEN-FLUX-DEVIANT-1", lambda d: sensibilite(d, DEVIANT)["lignes"])}


def main(argv: list) -> int:
    """sens_pool.py {quasi-mort | deviant} --journaux D --sortie F (options de commun.executer)."""
    quoi, *reste = argv
    items, analyse = ANALYSES[quoi]
    return commun.executer(f"sens_pool.py {quoi}", items, analyse, reste)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
