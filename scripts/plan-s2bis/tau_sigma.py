"""TAU-SIGMA-S2BIS (G0 du lot PLAN-S2BIS, sortie 1 ; SHOGEN-TAU-REDERIV-1) : τ_c et σ_c par classe de source, BTC/USD
seul, segment J28 de S2, plage D5 exclue, règle d'ADR-0029 §2.6 (l.178-180, recopiée dans parametres.json) et
adjudications A-1, A-2 de l'orchestrateur (2026-10-04). Population de τ : cellules (fenêtre, flux) du pool D1-bis de la
strate que r1._classify_window, sous les σ et τ committés de S2, classe HORS_ENVELOPPE ou PAS_ECART (axe (i) atteint) ;
rapport par r1._ecart_relatif sur les répondantes du pool D1-bis. Staleness t_fin(j) − source_ts sur deux populations :
(B) de clôture, répondantes (statut ok, prix) du pool D1-bis à horodatage porté (règle de clôture d'ADR-0021) ; (A) de
l'axe (i). La clé sigma_population désigne celle du paquet ; l'autre est imprimée, descriptive. Valeurs destinées au
paquet de S2-bis, jamais re-réglées ensuite."""
from __future__ import annotations

from decimal import Decimal, localcontext

import commun
import regles

ITEMS = "TAU-SIGMA-S2BIS (ADR-0029 §2.6 ; SHOGEN-TAU-REDERIV-1)"
NOMS = {"cloture": "(B) de clôture", "axe_i": "(A) de l'axe (i)"}


def populations(par: dict, d: dict) -> dict:
    """{(classe, strate) : (rapports de l'axe (i), staleness (A) de l'axe (i), staleness (B) de clôture)} : (B) compte les
    répondantes horodatées périmées ou non évaluables, que (A) écarte (closure.compute_closure, cité)."""
    r1, fin, out = commun.H["r1"], commun.H["window"].window_end, {}
    axe_i = (r1.Ecart.HORS_ENVELOPPE, r1.Ecart.PAS_ECART)
    with localcontext(r1.contexte_decimal()):
        for st, fenetres in par.items():
            for ws, cls, rep in fenetres:
                for f, e in cls.items():
                    rapports, axe, cloture = out.setdefault((d["scf"][f], st), ([], [], []))
                    ts = d["rmap"][ws, f].get("source_ts") if f in rep else None
                    age = None if ts is None else +(Decimal(fin(ws, d["w"])) - r1._as_dec(ts))
                    if age is not None:
                        cloture.append(age)
                    if e in axe_i:
                        rapports.append(r1._ecart_relatif(rep, f))
                        if age is not None:
                            axe.append(age)
    return out


def regle(pops: dict, prm: dict, classes: list, sigma_s2: dict) -> dict:
    """Par classe : τ (P99,9 au rang ⌈999·N/1000⌉, maximum sur les strates, grille, bornes), τ de la règle au maximum
    (descriptif), σ sur chaque population (P99, maximum sur les strates, plancher), détail par strate avec le nombre de
    cellules (B) au-delà du σ committé de S2 (sigma_s2, comparaison stricte comme r1.classify_ecart)."""
    t, s, out = prm["tau"], prm["sigma"], {}
    if prm["sigma_population"] not in NOMS:
        raise ValueError(f"sigma_population {prm['sigma_population']!r} hors de {sorted(NOMS)} — fail-closed")
    bornes = [Decimal(t[k]) for k in ("pas", "borne_basse", "borne_haute_exclue")]
    for c in classes:
        par, s2 = {}, sigma_s2.get(c)
        for st in prm["strates"]:
            r, za, zb = pops.get((c, st), ([], [], []))
            par[st] = {"N": len(r), "p999": regles.quantile(r, *t["quantile"]), "p99": regles.quantile(r, 99, 100),
                       "max": max(r, default=None), "N_a": len(za), "p99_a": regles.quantile(za, *s["quantile"]),
                       "N_b": len(zb), "p99_b": regles.quantile(zb, *s["quantile"]),
                       "au_dela": None if s2 is None else sum(z > s2 for z in zb)}
        p999 = max((v["p999"] for v in par.values() if v["p999"] is not None), default=None)
        pmax = max((v["max"] for v in par.values() if v["max"] is not None), default=None)
        sig = {k: regles.regle_sigma(Decimal(s["facteur"]), [v["p99_" + k] for v in par.values()], s["planchers_s"][c])
               for k in "ab"}
        out[c] = {"strates": par, "p999": p999, "pmax": pmax, "sigma_axe_i": sig["a"], "sigma_cloture": sig["b"],
                  "tau": regles.regle_tau(Decimal(t["facteur"]), p999, *bornes),
                  "tau_max": regles.regle_tau(Decimal(t["facteur"]), pmax, *bornes)}
    return out


def valeurs_paquet(v: dict, classes: list, prm: dict) -> list:
    """Bloc machine : « tau <classe> <τ> », ou REFUS nommé avec la valeur de la règle à la borne haute, jamais une valeur
    écrêtée (A-2), ou « - » sans cellule ; « sigma <classe> <σ> » de la population désignée par sigma_population (A-1)."""
    dec, haute, out = commun.dec, prm["tau"]["borne_haute_exclue"], []
    for c in classes:
        tau, _drapeau, brut = v[c]["tau"]
        out.append(f"tau {c} {dec(tau)}" if tau is not None else f"tau {c} - (aucune cellule)" if brut is None else
                   f"tau {c} REFUS {dec(brut)} (valeur de la règle, ≥ borne haute exclue {haute})")
    for c in classes:
        sig = v[c]["sigma_" + prm["sigma_population"]][0]
        out.append(f"sigma {c} {'aucun' if sig is None else dec(sig)}")
    return out


def analyse(d: dict, prm: dict) -> list:
    dec, H = commun.dec, commun.H
    unites = list(prm["pool_d1bis"]["unites"].values())
    classes = sorted({d["scf"][f] for f in unites})
    v = regle(populations(commun.classer(d, d["pools_bis"]), d), prm, classes, d["sbc"])
    choix = prm["sigma_population"]
    lignes = ["[TAU-SIGMA-S2BIS] BTC/USD seul ; population de τ : cellules arrivées à l'axe (i) sous le σ de S2, pool "
              f"D1-bis de la strate ; σ au paquet : population {NOMS[choix]} ; valeurs destinées au paquet de S2-bis, jamais "
              "re-réglées ensuite (ADR-0029 §2.6 ; adjudications A-1 et A-2 de l'orchestrateur, 2026-10-04)"]
    for c in classes:
        x, s2, plancher = v[c], d["sbc"].get(c), prm["sigma"]["planchers_s"][c]
        lignes.append(f"classe « {c} » : unités D1-bis {', '.join(f for f in unites if d['scf'][f] == c)} ; τ committé de "
                      f"S2 {dec(d['tau'].get(c))} ; σ committé de S2 {'aucun' if s2 is None else dec(s2) + ' s'}")
        for st, e in x["strates"].items():
            lignes += [f"  « {st} » : N = {e['N']} cellules à l'axe (i) ; P99,9 = {dec(e['p999'])} ; P99 = "
                       f"{dec(e['p99'])} ; maximum = {dec(e['max'])}",
                       f"  « {st} » staleness : population {NOMS['cloture']} N = {e['N_b']}, au-delà du σ de S2 "
                       f"{dec(e['au_dela'])}, P99 = {dec(e['p99_b'])} s ; population {NOMS['axe_i']} N = {e['N_a']}, "
                       f"P99 = {dec(e['p99_a'])} s"]
        (tau, dt, brut), (tmax, dm, _bm) = x["tau"], x["tau_max"]
        with localcontext(H["r1"].contexte_decimal()):
            txt = f"{tau} ({tau * 100} %)" if tau is not None else "-" if brut is None else "REFUS"
        lignes += [f"  τ_c = {txt} = grid-ceil({prm['tau']['facteur']} × max_s P99,9 = {dec(x['p999'])}, "
                   f"{prm['tau']['pas']}) ; bornes : {dt or 'non atteintes'}",
                   f"  τ de la règle au maximum (descriptif, hors paquet) = {'REFUS' if tmax is None else dec(tmax)} "
                   f"(grid-ceil({prm['tau']['facteur']} × {dec(x['pmax'])})) ; bornes : {dm or 'non atteintes'}"]
        for k in (choix, *(k for k in NOMS if k != choix)):
            sig, ds = x["sigma_" + k]
            lignes.append(f"  σ{'_c' if k == choix else ''}, population {NOMS[k]} "
                          f"({'au paquet' if k == choix else 'descriptif, hors paquet'}) = "
                          f"{'aucun' if sig is None else dec(sig) + ' s'} = max(plancher "
                          f"{'aucun' if plancher is None else plancher}, {prm['sigma']['facteur']} × max_s P99 staleness) ; "
                          f"{ds or 'règle appliquée'}")
    lignes += ["limite écrite : population (A) censurée à σ_S2 : σ_c ≤ max(plancher, 3 × σ_S2) par construction "
               "(adjudication A-1) ; pour Chainlink (heartbeat d'environ 1 h), σ = 3 × P99 de la staleness rend l'axe "
               "staleness presque aveugle par construction (ADR-0029 §2.6) ; choix de conception",
               "[VALEURS POUR LE PAQUET DE S2-BIS]"]
    lignes += valeurs_paquet(v, classes, prm)
    return lignes


def main(argv=None) -> int:
    return commun.executer("tau_sigma", ITEMS, analyse, argv)


if __name__ == "__main__":
    raise SystemExit(main())
