"""SHOGEN-SIM-NIVEAU-MODELES-1 (lot DETTES-SIM, 2026-10-04) : niveau de z_s, z_bloc,s et de la règle SHOGEN-CRITERE-R1-1
sous trois extensions du modèle nul de SIM-NIVEAU (G0-lot-SIM-NIVEAU l.239) : (a) fenêtres absentes ; (b) hétérogénéité
(p_i, L_i) ; (c) durées d'écart à queue lourde. Cas, R, graine : pré-enregistrement du lot (journal G1
docs/G1-lot-DETTES-SIM.md). Réplication : sim_dettes_calc.serie_modele puis stats. Oracles internes (fail-closed,
5 SE) : K/n contre P_more des marges ; p̄ par groupe de flux ; run d'écart moyen par groupe (p, L, loi) contre
nL/(n + L − 1) (L = 1 : n/(1 + (n − 1)(1 − p)) ; queue lourde : L = E[D]) ; fraction présente contre 0,9 (a).
Oracle externe : sim_dettes_oracle_r1.py. Usage : python3.13 -B sim_modeles.py --sortie DOSSIER [--processus k]
[--diviseur d]      Worker G1 DETTES-SIM, claude-opus-5-5."""
import argparse, hashlib, math, os, sys, time
from collections import Counter
from fractions import Fraction
from statistics import NormalDist

import sim_dettes_calc as D3
import sim_dettes_commun as D
import sim_niveau as S
import sim_niveau_calc as C

CAS = (*(("a", L, T) for L in (1, 20, 60) for T in (11112, 27778)),
       *(("b", L, n) for L in ("1", "20", "mele") for n in (10000, 25000)),
       *(("c", L, n) for L in (5, 20, 60) for n in (10000, 25000)))
R0, DIV_PREFIXE, ITEM = 4000, 20, "SHOGEN-SIM-NIVEAU-MODELES-1"
CONSEQUENCE = ("Conséquence pré-déclarée (lot DETTES-SIM ; G0-lot-SIM-NIVEAU l.239, C-6) : cette sortie ne modifie ni ℓ, ni "
               "le seuil, ni la règle ; un niveau mesuré au-dessus de 0,01 devient une limite écrite, jamais une révision. "
               "Ajoutée après l'exécution unique ; synthétique ; paramètres de conception seuls ; hors décision.")


def tache(args):
    cas, r = args
    return D3.stats(*D3.serie_modele(cas, r))


def specs(cas):
    """(p_i, L_i, loi) des 11 flux du cas."""
    ext, L, _ = cas
    if ext == "b":
        return [(p, Li, "markov") for p, Li in zip(D3.HETERO, D3.MELE if L == "mele" else (int(L),) * 11)]
    return [(0.02, L, "markov" if ext == "a" else "lourd")] * 11


def run_theorique(p, L, loi, n):
    pf = Fraction(p)
    if loi == "markov" and L == 1:
        return Fraction(n) / (1 + (n - 1) * (1 - pf))
    Le = Fraction(D3.LOURD[L][1]) if loi == "lourd" else Fraction(L)
    return n * Le / (n + Le - 1)


def agreger(cas, R, recs):
    sp, T = specs(cas), cas[2]
    gr = {g: [i for i, s in enumerate(sp) if s == g] for g in sorted(set(sp), key=str)}
    h, hp, c, zs, zbs, ctl, kn, pres, ns = hashlib.sha256(), hashlib.sha256(), Counter(), [], [], [], [], [], []
    pg, rg = {g: [] for g in gr}, {g: Counter() for g in gr}
    for r, d in enumerate(recs):
        rec, ligne = D3.publique(r, d)
        h.update(ligne.encode("utf-8"))
        if r < R // DIV_PREFIXE:
            hp.update(ligne.encode("utf-8"))
        if r < 10:
            ctl.append(rec)
        D3.compter(c, d)
        n = d["n"]
        ns.append(n)
        kn.append(d["K"] / n)
        pres.append(n / T)
        for v, z in ((zs, d["z"]), (zbs, d["z_bloc"])):
            if z is not None:
                v.append(float(z))
        for g, ix in gr.items():
            pg[g].append(sum(d["e"][i] for i in ix) / (len(ix) * n))
            X, Y = sum(d["e_grille"][i] for i in ix), sum(d["runs"][i] for i in ix)
            rg[g].update({"X": X, "Y": Y, "X2": X * X, "Y2": Y * Y, "XY": X * Y})
    pm = 1 - math.prod(1 - Fraction(p) for p, _, _ in sp) - sum(
        Fraction(p) * math.prod(1 - Fraction(q) for j, (q, _, _) in enumerate(sp) if j != i) for i, (p, _, _) in enumerate(sp))
    (mk, sk), (mp, spr) = D.moy_se(kn), D.moy_se(pres)
    o = [D.controle("K/n contre P_more des marges", mk, float(pm), sk)]
    for g, ix in gr.items():
        m, se = D.moy_se(pg[g])
        o.append(D.controle(f"p̄ du groupe {g}", m, g[0], se))
        s = rg[g]
        rl = Fraction(s["X"], s["Y"])
        vd = (s["X2"] - 2 * rl * s["XY"] + rl * rl * s["Y2"]) / (R - 1)
        o.append(D.controle(f"run d'écart moyen du groupe {g}", float(rl), float(run_theorique(*g, T)),
                            math.sqrt(vd / R) / (s["Y"] / R)))
    if cas[0] == "a":
        o.append(D.controle("fraction présente contre 1 − f", mp, 1 - D3.TROU[0], spr))
    if c["R"] != R or min(ns) < C.N_MIN_BLOCS:
        raise RuntimeError(f"{c['R']} enregistrements pour R = {R}, ou n < 30ℓ : {cas}")
    (mz, sz), (mzb, szb) = S.moy_sd(zs), S.moy_sd(zbs)
    return {"cas": list(cas), "L": cas[1], "n": min(ns), "n_moyen": sum(ns) / R, "comptes": {"R": R, **{k: c[k] for k in
            S.COMPTES}}, "taux": {"z": S.taux(c["z ≥ 2,33"], R), "z_bloc": S.taux(c["z_bloc ≥ 2,33"], R),
            "regle": S.taux(c["REJETTE"], R)}, "diagnostics": {"z_moyenne": mz, "z_sd": sz, "z_bloc_moyenne": mzb,
            "z_bloc_sd": szb}, "oracles_internes": o, "controle_premieres": ctl, "empreinte_sha256": h.hexdigest(),
            "prefixe_R": R // DIV_PREFIXE, "empreinte_prefixe": hp.hexdigest()}


def texte(ent):
    f4, tx = (lambda v: "—" if v is None else f"{v:.4f}"), (lambda u: f"{u['x']} → {u['r']:.5f} (SE {u['SE']:.5f})" + (
        f" [borne 95 % {u['borne95_si_x_nul']:.2e}]" if u["x"] == 0 else ""))
    t = [f"{ITEM} ({ent['schema']}) ; " + " ; ".join(f"{k} sha256 {v}" for k, v in ent["script_sha256"].items()),
         f"R = {ent['parametres']['R']} par cas ; ℓ = 240 ; REJETTE ⇔ z ≥ 2,33 ∧ z_bloc ≥ 2,33 ; garde n·P̂(1−P̂) ≥ 10 ; "
         f"z_bloc publiée ⇔ σ̂² > 0 ∧ n ≥ 7 200 ; α nominal {ent['alpha_nominal']:.8f} ; extensions : (a) trous "
         f"(fraction 0,1, durée moyenne 60) ; (b) p_i = 0,01 (flux 1-6), 0,04 (7-11) ; (c) Lomax discrète α = 1,5.",
         ent["consequence_predeclaree"],
         "cas | n moyen | garde non tenue | σ̂² = 0 | r_z | r_bloc | r_règle | discordances | NON ÉVALUABLE garde ; non "
         "qualifiable | SD(z) | SD(z_bloc) | run maximal de I ≥ ℓ | oracles internes (écart en SE)"]
    for k in ent["cas"]:
        c, u, g = k["comptes"], k["taux"], k["diagnostics"]
        t.append(f"{k['cas']} | {k['n_moyen']:.1f} | {c['garde non tenue']} | {c['σ̂² = 0']} | {tx(u['z'])} | "
                 f"{tx(u['z_bloc'])} | {tx(u['regle'])} | {c['NE REJETTE PAS (discordance)']} | "
                 f"{c['NON ÉVALUABLE (garde §5.4)']} ; {c['NON ÉVALUABLE (rejet non qualifiable)']} | {f4(g['z_sd'])} | "
                 f"{f4(g['z_bloc_sd'])} | {c['run maximal de I ≥ ℓ']} | "
                 + " ; ".join(f"{o['ecart_en_SE']:+.2f}" for o in k["oracles_internes"])
                 + f" | empreinte {k['empreinte_sha256']} ; préfixe {k['prefixe_R']} {k['empreinte_prefixe']}")
    return "\n".join(t) + "\n"


def main():
    ap = argparse.ArgumentParser(description=ITEM + " (lot DETTES-SIM)")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--processus", type=int, default=1)
    ap.add_argument("--diviseur", type=int, default=1)
    a = ap.parse_args()
    ch = D.chemins(a.sortie, "modeles")
    sh = D.shas(os.path.abspath(__file__), D3.__file__, D.__file__, S.__file__, C.__file__)
    R, debut, journal, res = R0 // a.diviseur, time.gmtime(), [], []
    with D.pool(a.processus) as pl:
        for cas in CAS:
            t0 = time.perf_counter()
            try:
                res.append(agreger(cas, R, D.imap(pl, tache, ((cas, r) for r in range(R)), 10)))
            except RuntimeError as exc:
                sys.exit(f"ECHEC D'ORACLE, aucun fichier ecrit : {exc}")
            journal.append(f"cas {cas} R={R} : {time.perf_counter() - t0:.1f} s (horloge murale)")
            print(journal[-1], file=sys.stderr, flush=True)
    ent = {"schema": "shogen.sim-modeles.v1", "item": ITEM, "script_sha256": sh, "etiquette": D.ETIQUETTE,
           "journal": "docs/G1-lot-DETTES-SIM.md, pré-enregistrement",
           "parametres": {"R": R, "diviseur": a.diviseur, "cas": [list(x) for x in CAS], "trou": list(D3.TROU),
                          "lourd_d0_ED": {str(k): list(v) for k, v in D3.LOURD.items()}, "alpha": D3.ALPHA,
                          "hetero": list(D3.HETERO), "mele": list(D3.MELE), "graine": D3.GRAINE,
                          "chaine": "SHOGEN-DETTES-SIM-MODELES|{graine}|{ext}|L={L}|{taille}|r={r}",
                          "prefixe": f"R/{DIV_PREFIXE}"},
           "alpha_nominal": 1 - NormalDist().cdf(2.33), "consequence_predeclaree": CONSEQUENCE, "cas": res}
    D.ecrire(ch, ent, texte(ent), a.processus, debut, journal)


if __name__ == "__main__":
    main()
