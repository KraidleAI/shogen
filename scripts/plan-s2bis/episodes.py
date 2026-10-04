"""Épisodes (G0 du lot PLAN-S2BIS, sortie 2 ; ADR-0029 §6 lot 3) : distributions des longueurs d'épisodes de panne et
d'écart par unité du pool D1-bis, et courbe FIV_série(ℓ), pour calibrer SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS ; descriptif.

Définitions fixées avant toute exécution sur les journaux (parametres.json, clé episodes et fiv) : classement de
r1._classify_window sous les σ et τ committés de S2 ; épisode = suite maximale de positions de grille consécutives (pas
w) parmi les fenêtres retenues de la strate où la cellule de l'unité est du type (panne : PANNE ; écart : PANNE,
STALENESS ou HORS_ENVELOPPE) ; une fenêtre absente, exclue ou de l'autre strate coupe l'épisode (forme des runs de
r1.bloc_strate) ; épisode censuré : fenêtre de grille voisine (avant ou après) non retenue dans la strate. FIV_série(ℓ) =
σ̂²_bloc(ℓ)/γ̂₀ de r1.block_long_run_variance (forme de r1.bloc_strate) sur la série I_t = 1{au moins deux écarts}, pour
le pool S2 (D1, celui du rendu) et le pool D1-bis ; à ℓ = r1.ELL_BLOC, K et FIV_série du pool S2 doivent égaler le bloc
de r1.compute_r1 (sinon refus)."""
from __future__ import annotations

from collections import Counter
from decimal import Decimal, localcontext

import commun
import regles

ITEMS = "épisodes de panne et d'écart, courbe FIV_série(ℓ) (ADR-0029 §6 lot 3 ; SIM-NIVEAU-BIS, SIM-PUISSANCE-BIS)"


def episodes(fenetres: list, w: int, pred) -> list:
    """[(longueur, censuré au début, censuré à la fin)] des suites maximales de positions de grille consécutives (écart
    w) de `fenetres` ([(ws, x)] d'une strate) où pred(x) est vrai."""
    vus = {ws for ws, _x in fenetres}
    oui = {ws for ws, x in fenetres if pred(x)}
    out = []
    for ws in sorted(oui):
        if ws - w in oui:
            continue
        fin = ws
        while fin + w in oui:
            fin += w
        out.append(((fin - ws) // w + 1, ws - w not in vus, fin + w not in vus))
    return out


def resume(eps: list, n_s: int, quantiles: list) -> dict:
    """Comptes, taux (cellules / n_s), moyenne, maximum, quantiles au rang le plus proche, censurés, complets et leur
    moyenne, histogramme [(longueur, nombre)]."""
    lg = [x[0] for x in eps]
    comp = [x[0] for x in eps if not (x[1] or x[2])]
    with localcontext(commun.H["r1"].contexte_decimal()):
        return {"episodes": len(lg), "cellules": sum(lg), "max": max(lg, default=None),
                "taux": +(Decimal(sum(lg)) / Decimal(n_s)) if n_s else None,
                "moyenne": +(Decimal(sum(lg)) / Decimal(len(lg))) if lg else None,
                "q": [regles.quantile(lg, a, b) for a, b in quantiles], "censures": len(lg) - len(comp),
                "complets": len(comp), "moyenne_complets": +(Decimal(sum(comp)) / Decimal(len(comp))) if comp else None,
                "histogramme": sorted(Counter(lg).items())}


def serie(fenetres: list) -> list:
    """[(ws, I_t)] : I_t = 1 si au moins deux écarts dans la fenêtre (même sommande que K de compute_r1)."""
    e = commun.H["r1"].ECARTS
    return [(ws, int(sum(x in e for x in cls.values()) >= 2)) for ws, cls, _rep in fenetres]


def courbe(s: list, w: int, ells: list) -> list:
    """Par ℓ : n, K, FIV_série = σ̂²_bloc/γ̂₀ (None si n = 0 ou γ̂₀ = 0), σ̂²_bloc, γ̂₀, cv théorique √(4ℓ/(3n)) et garde
    n ≥ GARDE_BLOCS·ℓ."""
    r1, out = commun.H["r1"], []
    for ell in ells:
        v = r1.block_long_run_variance(s, w, ell)
        with localcontext(r1.contexte_decimal()):
            fs = None if not v["n"] or v["gamma0"] == 0 else +(v["sigma2_bloc"] / v["gamma0"])
            cv = +(Decimal(4 * ell) / Decimal(3 * v["n"])).sqrt() if v["n"] else None
        out.append({"ell": ell, "n": v["n"], "K": v["K"], "FIV_serie": fs, "sigma2_bloc": v["sigma2_bloc"],
                    "gamma0": v["gamma0"], "cv": cv, "garde": v["n"] >= r1.GARDE_BLOCS * ell})
    return out


def controle_fiv(par_s2: dict, d: dict) -> list:
    """Strates où (K, FIV_série) de la série recalculée sur le pool S2, à ℓ = r1.ELL_BLOC, diffèrent du bloc de
    compute_r1 (sortie « base »)."""
    ell, out = commun.H["r1"].ELL_BLOC, []
    for st, b in d["base"]["strates"].items():
        c = courbe(serie(par_s2.get(st, [])), d["w"], [ell])[0]
        if (c["K"], c["FIV_serie"]) != (b["K"], b["bloc"]["FIV_serie"]):
            out.append(st)
    return out


def analyse(d: dict, prm: dict) -> list:
    r1, dec = commun.H["r1"], commun.dec
    types = {nom: {r1.Ecart(v) for v in vals} for nom, vals in prm["episodes"]["types"].items()}
    qs = prm["episodes"]["quantiles"]
    par_bis, par_s2 = commun.classer(d, d["pools_bis"]), commun.classer(d, d["pools_s2"])
    ecarts = controle_fiv(par_s2, d)
    if ecarts:
        raise ValueError(f"FIV_série recalculée différente du bloc de compute_r1 (strates {ecarts}) — fail-closed")
    lignes = ["[ÉPISODES] descriptif, pour calibrer SIM-NIVEAU-BIS et SIM-PUISSANCE-BIS ; classement sous les σ et τ "
              "committés de S2 ; unités du pool D1-bis de la strate ; quantiles au rang le plus proche (P"
              + ", P".join(str(a) for a, _b in qs) + ")"]
    for st in prm["strates"]:
        fen = par_bis.get(st, [])
        if st not in d["pools_bis"]:
            lignes.append(f"  « {st} » : aucune fenêtre retenue dans la strate")
            continue
        for h, f in prm["pool_d1bis"]["unites"].items():
            if f not in d["pools_bis"][st]:
                lignes.append(f"  « {st} » {f} (hôte {h}) : hors du pool D1-bis de la strate")
                continue
            for nom, ens in types.items():
                r = resume(episodes([(ws, cls[f]) for ws, cls, _rep in fen], d["w"], ens.__contains__), len(fen), qs)
                lignes += [f"  « {st} » {f} (hôte {h}) {nom} : n_s = {len(fen)} ; cellules = {r['cellules']} ; épisodes = "
                           f"{r['episodes']}, dont censurés {r['censures']} ; taux = {dec(r['taux'])} ; moyenne = "
                           f"{dec(r['moyenne'])} ; max = {dec(r['max'])} ; " + " ; ".join(
                               f"P{a} = {dec(v)}" for (a, _b), v in zip(qs, r["q"])) + f" ; complets : {r['complets']}, "
                           f"moyenne {dec(r['moyenne_complets'])}",
                           "    histogramme (longueur×nombre) : " + (" ".join(f"{k}×{v}" for k, v in r["histogramme"])
                                                                      or "aucun épisode")]
    lignes.append(f"[FIV_SÉRIE(ℓ)] σ̂²_bloc(ℓ)/γ̂₀, série I_t = 1{{au moins deux écarts}} ; garde n ≥ {r1.GARDE_BLOCS}·ℓ "
                  f"imprimée ; pool S2 contrôlé égal au bloc de compute_r1 à ℓ = {r1.ELL_BLOC}")
    for nom, par in (("S2 (D1)", par_s2), ("D1-bis", par_bis)):
        for st in prm["strates"]:
            for c in courbe(serie(par.get(st, [])), d["w"], prm["fiv"]["ell"]):
                lignes.append(f"  {nom} « {st} » ℓ = {c['ell']} : n = {c['n']} ; K = {c['K']} ; FIV_série = "
                              f"{dec(c['FIV_serie'])} ; σ̂²_bloc = {dec(c['sigma2_bloc'])} ; γ̂₀ = {dec(c['gamma0'])} ; cv "
                              f"théorique = {dec(c['cv'])} ; garde : {'tenue' if c['garde'] else 'non tenue'}")
    return lignes


def main(argv=None) -> int:
    return commun.executer("episodes", ITEMS, analyse, argv)


if __name__ == "__main__":
    raise SystemExit(main())
