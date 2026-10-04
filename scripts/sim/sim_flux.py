"""SHOGEN-FLUX-QUASI-MORT-2 et SHOGEN-FLUX-FAIBLE-1 (lot DETTES-SIM, 2026-10-04) : point de bascule du signal et puissance
de la règle SHOGEN-CRITERE-R1-1 selon le profil des taux d'écart, sur données synthétiques (11 flux, fenêtres iid,
n = 10⁴). Alternative fixée au pré-enregistrement (journal G1 docs/G1-lot-DETTES-SIM.md) : choc commun S_t ~ Bernoulli(q)
sur la paire (flux 1, 2), marge p = 0,02 conservée ; profils : k flux faibles (flux 3 à 2 + k) au taux p_w, autres à p ;
chacun sous le nul (q = 0) et sous l'alternative ; une suite de tirages par réplication, commune aux 40 profils.
Référence exacte (dérivation du worker, contrôlée ici à 5 SE) : E[K − n·P̂_more] = (n − 1)·c·(r₀ − r₁), r₀ et r₁ =
P(0 et 1 écart hors de la paire) ; 0 sous le nul. Oracle externe : sim_dettes_oracle_r1.py.
Usage : python3.13 -B sim_flux.py --sortie DOSSIER [--processus k] [--diviseur d]   Worker G1 DETTES-SIM."""
import argparse, hashlib, math, os, sys, time
from collections import Counter
from fractions import Fraction
from statistics import NormalDist

import sim_dettes_calc as D3
import sim_dettes_commun as D
import sim_niveau as S
import sim_niveau_calc as C

G13 = (0.0, 0.1, 0.2, 0.25, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.75, 0.9, 1.0)
PROFILS = ((0, None), *((1, w) for w in G13), *((k, w) for k in (2, 4) for w in (0.1, 0.25, 0.4)))
N, P, Q, R0, DIV_PREFIXE, ITEM = 10000, 0.02, 0.006667, 4000, 20, "SHOGEN-FLUX-QUASI-MORT-2 ; SHOGEN-FLUX-FAIBLE-1"
PP = (P - Q) / (1 - Q)
CF = (Fraction(Q) + (1 - Fraction(Q)) * Fraction(PP) ** 2) - (Fraction(Q) + (1 - Fraction(Q)) * Fraction(PP)) ** 2
CONSEQUENCE = ("Conséquence pré-déclarée (lot DETTES-SIM ; AVIS-SEUIL-FLUX-QUASI-MORT L1, L3) : cette sortie ne modifie "
               "ni le seuil 1/2 de SHOGEN-FLUX-QUASI-MORT-1, ni ℓ, ni le seuil 2,33, ni la règle. Ajoutée après "
               "l'exécution unique ; synthétique ; hors décision ; rien n'est établi sur des sources réelles (doc 09).")


def ps(k, w):
    return [P, P] + [P if (k == 0 or j >= k) else w for j in range(9)]


def tache(r):
    U, cache, out = D3.base_flux(N, r), {}, []
    for k, w in PROFILS:
        for al in (False, True):
            d = D3.stats(D3.profil(U, ps(k, w), Q if al else 0, cache), None)
            out.append({x: d[x] for x in ("n", "K", "e", "N", "P_more", "tenue", "z", "z_bloc", "x", "valeur", "rmax")})
    return out


def r0_r1(reste):
    f = [Fraction(x) for x in reste]
    return math.prod(1 - x for x in f) - sum(x * math.prod(1 - y for j, y in enumerate(f) if j != i) for i, x in enumerate(f))


def agreger(R, recs):
    nb = 2 * len(PROFILS)
    h, hp, c, xs, kn = [hashlib.sha256() for _ in range(nb)], [hashlib.sha256() for _ in range(nb)], [
        Counter() for _ in range(nb)], [[] for _ in range(nb)], [[] for _ in range(nb)]
    ctl = [[] for _ in range(nb)]
    for r, rep in enumerate(recs):
        for j, d in enumerate(rep):
            rec, ligne = D3.publique(r, d)
            h[j].update(ligne.encode("utf-8"))
            if r < R // DIV_PREFIXE:
                hp[j].update(ligne.encode("utf-8"))
            if r < 3:
                ctl[j].append(rec)
            D3.compter(c[j], d)
            xs[j].append(float(d["x"]))
            kn[j].append(d["K"] / d["n"])
    base, cas = r0_r1(ps(0, None)[2:]), []
    for j, ((k, w), al) in enumerate((pr, al) for pr in PROFILS for al in (False, True)):
        p_ = ps(k, w)
        pm = 1 - math.prod(1 - Fraction(x) for x in p_) - sum(
            Fraction(x) * math.prod(1 - Fraction(y) for i, y in enumerate(p_) if i != m) for m, x in enumerate(p_))
        f = r0_r1(p_[2:])
        ex = (N - 1) * CF * f if al else Fraction(0)
        (mx, sx), (mk, sk) = D.moy_se(xs[j]), D.moy_se(kn[j])
        o = [D.controle("moyenne de K − nP̂ contre l'excès exact", mx, float(ex), sx)]
        if not al:
            o.append(D.controle("K/n contre P_more des marges", mk, float(pm), sk))
        cas.append({"k": k, "p_w": w, "alternative": al, "L": 1, "n": N, "comptes": {"R": R, **{x: c[j][x] for x in
                    S.COMPTES}}, "taux": {"z": S.taux(c[j]["z ≥ 2,33"], R), "z_bloc": S.taux(c[j]["z_bloc ≥ 2,33"], R),
                    "regle": S.taux(c[j]["REJETTE"], R)},
                    "exact": {"P_more_marges": float(pm), "exces": float(ex), "facteur_exact": float(f / base),
                              "facteur_naif": (1 - 2 * w) ** k if k else 1.0},
                    "mesure": {"exces_moyen": mx, "exces_SE": sx, "exces_normalise": mx / ((N - 1) * float(CF)),
                               "exces_normalise_SE": sx / ((N - 1) * float(CF))},
                    "oracles_internes": o, "controle_premieres": ctl[j], "empreinte_sha256": h[j].hexdigest(),
                    "prefixe_R": R // DIV_PREFIXE, "empreinte_prefixe": hp[j].hexdigest()})
    return cas, bascule(cas, xs, R)


def bascule(cas, xs, R):
    """Premier changement de signe (+ vers −) de la moyenne de K − nP̂ sous l'alternative, k = 1, dans l'ordre de G13 ;
    interpolation linéaire ; SE par la méthode delta sur les réplications appariées (nombres aléatoires communs)."""
    ix = [j for j, x in enumerate(cas) if x["k"] == 1 and x["alternative"]]
    for a, b in zip(ix, ix[1:]):
        m1, m2 = cas[a]["mesure"]["exces_moyen"], cas[b]["mesure"]["exces_moyen"]
        if m1 > 0 >= m2:
            w1, w2 = cas[a]["p_w"], cas[b]["p_w"]
            g1, g2 = (w2 - w1) * -m2 / (m1 - m2) ** 2, (w2 - w1) * m1 / (m1 - m2) ** 2
            v1, v2 = S.moy_sd(xs[a])[1] ** 2, S.moy_sd(xs[b])[1] ** 2
            c12 = math.fsum((x - m1) * (y - m2) for x, y in zip(xs[a], xs[b])) / (R - 1)
            return {"exacte": (1 - 9 * P) / (2 - 10 * P), "mesuree": w1 + (w2 - w1) * m1 / (m1 - m2),
                    "SE": math.sqrt(max(g1 * g1 * v1 + g2 * g2 * v2 + 2 * g1 * g2 * c12, 0) / R), "encadrement": [w1, w2]}
    return {"exacte": (1 - 9 * P) / (2 - 10 * P), "mesuree": None, "SE": None, "encadrement": None}


def texte(ent):
    tx = lambda u: f"{u['x']} → {u['r']:.5f} (SE {u['SE']:.5f})" + (f" [borne 95 % {u['borne95_si_x_nul']:.2e}]"
                                                                   if u["x"] == 0 else "")
    pa, b = ent["parametres"], ent["bascule"]
    t = [f"{ITEM} ({ent['schema']}) ; " + " ; ".join(f"{k} sha256 {v}" for k, v in ent["script_sha256"].items()),
         f"n = {N} ; fenêtres iid ; R = {pa['R']} ; alternative : q = {Q}, p′ = {PP!r}, c = {pa['c']:.10f} ; excès "
         f"normalisé = moyenne de (K − nP̂)/((n − 1)c) ; facteur exact = (r₀ − r₁)/(r₀ − r₁ de base) ; α nominal "
         f"{ent['alpha_nominal']:.8f}.", ent["consequence_predeclaree"],
         f"Bascule (k = 1, alternative) : mesurée {b['mesuree']} (SE {b['SE']}), entre {b['encadrement']} ; exacte "
         f"(1 − 9p)/(2 − 10p) = {b['exacte']:.6f} ; valeur de l'avis : 1/2.",
         "k | p_w | alternative | excès normalisé (SE) | exact normalisé | facteur exact ; naïf (1 − 2p_w)^k | r_z | "
         "r_règle | garde non tenue | rejet non qualifiable | oracles internes (écart en SE)"]
    for x in ent["cas"]:
        m, e, u, c = x["mesure"], x["exact"], x["taux"], x["comptes"]
        t.append(f"{x['k']} | {x['p_w']} | {x['alternative']} | {m['exces_normalise']:+.4f} ({m['exces_normalise_SE']:.4f}) "
                 f"| {e['exces'] / ((N - 1) * pa['c']):+.4f} | {e['facteur_exact']:+.4f} ; {e['facteur_naif']:+.4f} | "
                 f"{tx(u['z'])} | {tx(u['regle'])} | {c['garde non tenue']} | "
                 f"{c['NON ÉVALUABLE (rejet non qualifiable)']} | " + " ; ".join(f"{o['ecart_en_SE']:+.2f}" for o in
                                                                              x["oracles_internes"])
                 + f" | {x['empreinte_sha256']} ; préfixe {x['prefixe_R']} {x['empreinte_prefixe']}")
    return "\n".join(t) + "\n"


def main():
    ap = argparse.ArgumentParser(description=ITEM + " (lot DETTES-SIM)")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--processus", type=int, default=1)
    ap.add_argument("--diviseur", type=int, default=1)
    a = ap.parse_args()
    ch = D.chemins(a.sortie, "flux")
    sh = D.shas(os.path.abspath(__file__), D3.__file__, D.__file__, S.__file__, C.__file__)
    R, debut, t0 = R0 // a.diviseur, time.gmtime(), time.perf_counter()
    with D.pool(a.processus) as pl:
        try:
            cas, b = agreger(R, D.imap(pl, tache, range(R), 5))
        except RuntimeError as exc:
            sys.exit(f"ECHEC D'ORACLE, aucun fichier ecrit : {exc}")
    journal = [f"R={R} : {time.perf_counter() - t0:.1f} s (horloge murale)"]
    ent = {"schema": "shogen.sim-flux.v1", "item": ITEM, "script_sha256": sh, "etiquette": D.ETIQUETTE,
           "journal": "docs/G1-lot-DETTES-SIM.md, pré-enregistrement",
           "parametres": {"n": N, "p": P, "q": Q, "p_prime": PP, "c": float(CF), "R": R, "diviseur": a.diviseur,
                          "profils": [[k, w] for k, w in PROFILS], "graine": D3.GRAINE,
                          "chaine": "SHOGEN-DETTES-SIM-FLUX|{graine}|n={n}|r={r}", "prefixe": f"R/{DIV_PREFIXE}"},
           "alpha_nominal": 1 - NormalDist().cdf(2.33), "consequence_predeclaree": CONSEQUENCE, "cas": cas, "bascule": b}
    D.ecrire(ch, ent, texte(ent), a.processus, debut, journal)


if __name__ == "__main__":
    main()
