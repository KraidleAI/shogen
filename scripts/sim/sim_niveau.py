"""SHOGEN-SIM-NIVEAU-1, sous-lot SIM-NIVEAU-a2 : exécution, agrégation et sorties (G0 du lot, §4, §6, §7, §8).
Taux de rejet à tort à 2,33 de z, de z_bloc (ℓ = 240) et de la règle SHOGEN-CRITERE-R1-1 sous le modèle nul synthétique
de sim_niveau_calc (ADR-0028 §1 bis.1 pt 7 ; annexe A, ligne SIM-NIVEAU), avec l'erreur-type de Monte-Carlo par cas.
Oracles (2), (2b) et (5) exigés à l'exécution (fail-closed : sortie ≠ 0, aucun fichier écrit) ; (1) et (1b) par rejeu.
Usage : python -B sim_niveau.py --sortie DOSSIER [--processus k] ; --R, --p et --cas : essais et item P-1 seulement.
Rédaction : worker G1 claude-opus-5-5, 2026-09-30."""
import argparse, contextlib, hashlib, json, math, multiprocessing, os, platform, sys, time
from collections import Counter
from fractions import Fraction
from statistics import NormalDist, median

import sim_niveau_calc as C

P_DEFAUT, R_DEFAUT = 0.02, 100000
N_FLUX = 11  # G0 §2 ; constante de l'oracle (5), indépendante de sim_niveau_calc (code sous test)
CAS = [(L, n) for L in (1, 5, 20, 60) for n in (10000, 25000)]  # G0 §4 : L croissant, puis n croissant
VALEURS = ("REJETTE", "NE REJETTE PAS (z < 2,33)", "NE REJETTE PAS (discordance)", "NON ÉVALUABLE (garde §5.4)",
           "NON ÉVALUABLE (rejet non qualifiable)")
COMPTES = ("garde non tenue", "σ̂² = 0", "z_bloc non publiée", "z ≥ 2,33", "z_bloc ≥ 2,33", *VALEURS, "z ≤ −2,33",
           "z_bloc ≤ −2,33", "run maximal de I ≥ ℓ")
CONSEQUENCE = ("Conséquence pré-déclarée (ADR-0028 §1 bis.1 pt 7 ; C-6 du cp-1 de l'amendement) : cette sortie ne "
               "modifie ni ℓ, ni le seuil, ni la règle ; elle est imprimée avec l'erreur-type de Monte-Carlo de chaque "
               "cas ; tout changement de ℓ après sa lecture est un nouvel amendement daté, sous le veto §4.10 a. Ni p, "
               "ni R, ni la graine, ni les cas, ni les définitions des taux ne changent après la lecture d'une sortie "
               "(G0 §1). Niveau sous un modèle nul synthétique : rien n'est établi sur des sources réelles (doc 09).")


def taux(x, R):
    """x, r = x/R, SE = √(r(1−r)/R) ; si x = 0, borne unilatérale exacte à 95 % : 1 − 0,05^(1/R) (G0 §6)."""
    r = x / R
    return {"x": x, "r": r, "SE": math.sqrt(r * (1 - r) / R), "borne95_si_x_nul": 1 - 0.05 ** (1 / R) if x == 0 else None}


def ecart(nom, moyenne, theorie, se, **extra):
    """Oracle (5) : écart à la théorie en erreurs-types empiriques ; |écart| > 5 SE => arrêt, aucun fichier écrit."""
    k = (moyenne - theorie) / se if se > 0 else (0.0 if moyenne == theorie else math.inf)
    if not abs(k) <= 5:
        raise RuntimeError(f"oracle (5) {nom} : moyenne {moyenne!r}, theorie {theorie!r}, ecart {k!r} SE")
    return {"controle": nom, "moyenne": moyenne, "theorie": theorie, "SE": se, "ecart_en_SE": k, **extra}


def moy_sd(v):
    """Moyenne et écart-type (dénominateur len − 1), sommes math.fsum dans l'ordre des réplications."""
    if len(v) < 2:
        return None, None
    mu = math.fsum(v) / len(v)
    return mu, math.sqrt(math.fsum((x - mu) ** 2 for x in v) / (len(v) - 1))


def agreger(p, L, n, R, recs):
    """Comptes, taux, diagnostics et oracles d'un cas, dans l'ordre des r (G0 §6, §8) ; rend (cas, PID distincts)."""
    a, b = C.chaine(p, L)
    h, c, s, pids, zs, zbs = hashlib.sha256(), Counter(), Counter(), set(), [], []
    diag = {"FIV": [], "FIV_serie": [], "R_centrage": []}
    for r, d in enumerate(recs):
        if not (d["ok2"] and d["ok2b"]):
            raise RuntimeError(f"oracle (2) ou (2b) en echec : L={L} n={n} r={r}")
        h.update(d["ligne"].encode("utf-8"))
        X, Y, K = sum(d["e"]), sum(d["runs"]), d["K"]
        s.update({"R": 1, "K": K, "K2": K * K, "X": X, "X2": X * X, "Y": Y, "Y2": Y * Y, "XY": X * Y,
                  "runs_I": d["runs_I"], "rmax": d["rmax"]})
        c[d["valeur"]] += 1
        c["garde non tenue"] += not d["tenue"]
        c["σ̂² = 0"] += d["N"] == 0
        c["z_bloc non publiée"] += d["z_bloc"] is None
        c["run maximal de I ≥ ℓ"] += d["rmax"] >= C.ELL
        for cle, z, v in (("z", d["z"], zs), ("z_bloc", d["z_bloc"], zbs)):
            if z is not None:
                c[cle + " ≥ 2,33"] += z >= C.SEUIL_Z
                c[cle + " ≤ −2,33"] += z <= -C.SEUIL_Z
                v.append(float(z))
        for k, v in diag.items():
            if d[k] is not None:
                v.append(d[k])
        pids.add(d["pid"])
    if s["R"] != R:
        raise RuntimeError(f"{s['R']} enregistrements pour R = {R} : L={L} n={n}")
    pf = Fraction(p)                               # théories de (5) tirées du G0 §2, jamais de C.chaine (code sous test)
    pm_th = 1 - (1 - pf) ** N_FLUX - N_FLUX * pf * (1 - pf) ** (N_FLUX - 1)
    ln_th = Fraction(n, 1 + (n - 1) * (1 - pf)) if L == 1 else Fraction(n * L, n + L - 1)  # E[Σ_t D_t]/E[runs] (C-4)
    mom = {k: (Fraction(s[k], R), (s[k + "2"] - Fraction(s[k] ** 2, R)) / (R - 1)) for k in ("K", "X")}
    rl = Fraction(s["X"], s["Y"])                    # longueur moyenne des runs d'écart des 11 flux, rapport de sommes
    vd = (s["X2"] - 2 * rl * s["XY"] + rl * rl * s["Y2"]) / (R - 1)  # variance de X − rl·Y (linéarisation du rapport)
    o5 = [ecart("K/n contre P_more(p)", float(mom["K"][0] / n), float(pm_th), math.sqrt(mom["K"][1] / R) / n),
          ecart("p̄ = Σe/(11n) contre p", float(mom["X"][0] / (N_FLUX * n)), float(pf),
                math.sqrt(mom["X"][1] / R) / (N_FLUX * n)),
          ecart("run d'écart moyen Σe/Σruns contre L_n = nL/(n + L − 1), L = 1 : n/(1 + (n − 1)(1 − p))", float(rl),
                float(ln_th),
                math.sqrt(vd / R) / (s["Y"] / R), limite_n_infini=float(L if L > 1 else 1 / (1 - pf)))]
    (mz, sz), (mzb, szb) = moy_sd(zs), moy_sd(zbs)
    return {"L": L, "n": n, "a": a, "b": b, "rho": a - b, "rho_puissance_ell": (a - b) ** C.ELL,
            "P_more_theorique": float(pm_th), "comptes": {"R": R, **{k: c[k] for k in COMPTES}},
            "taux": {"z": taux(c["z ≥ 2,33"], R), "z_bloc": taux(c["z_bloc ≥ 2,33"], R), "regle": taux(c["REJETTE"], R)},
            "diagnostics": {"z_moyenne": mz, "z_sd": sz, "z_bloc_moyenne": mzb, "z_bloc_sd": szb,
                            **{k + "_mediane": (median(v) if v else None) for k, v in diag.items()},
                            "runs_I_moyen": s["runs_I"] / R,
                            "run_I_longueur_moyenne": s["K"] / s["runs_I"] if s["runs_I"] else None,
                            "run_I_max_moyen": s["rmax"] / R, "K_sur_n_moyen": float(mom["K"][0] / n)},
            "oracles": {"(2) n²γ̂₀ = n·K(n − K)": f"{R}/{R}", "(2b) N_lag = N_bloc": f"{R}/{R}", "(5)": o5},
            "empreinte_sha256": h.hexdigest()}, pids


def texte(ent):
    """Sortie texte (G0 §6) : en-tête, une ligne par cas, puis les oracles ; ni heure, ni durée (oracle 1)."""
    P, f4 = ent["parametres"], (lambda v: "—" if v is None else f"{v:.4f}")
    tx = (lambda u: f"{u['x']} → {u['r']:.6f} (SE {u['SE']:.6f})"
          + (f" [borne 95 % {u['borne95_si_x_nul']:.3e}]" if u["x"] == 0 else ""))
    t = ["SHOGEN-SIM-NIVEAU-1 (" + ent["schema"] + ") ; " + " ; ".join(f"{k} sha256 {v}" for k, v in ent["script_sha256"].items()),
         f"Paramètres : N = {P['N']} flux simulés, mutuellement indépendants par construction ; p = {P['p']} ; "
         f"R = {P['R']} ; ℓ = {P['ell']} ; REJETTE ⇔ z ≥ {P['seuil_z']} ∧ z_bloc ≥ {P['seuil_z']} ; garde tenue ⇔ "
         f"n·P̂(1−P̂) ≥ {P['garde_seuil']} ; z_bloc publiée ⇔ σ̂² > 0 ∧ n ≥ {P['garde_blocs_n_min']} ; graine "
         f"{P['graine']}, chaîne {P['chaine_graine']} (r = 0 du premier cas : {P['chaine_effective_r0']}) ; "
         f"Decimal, précision {P['decimal_prec']}.",
         f"α nominal = 1 − Φ(2,33) = {ent['alpha_nominal']:.8f}, pour comparaison ; aucun critère n'en est tiré (C-6).",
         ent["consequence_predeclaree"],
         "Taux sur les R réplications du cas : r_z = #{garde tenue ∧ z ≥ 2,33}/R ; r_bloc = #{z_bloc publiée ∧ z_bloc ≥ "
         "2,33}/R ; r_règle = #{REJETTE}/R ; SE = √(r(1−r)/R) ; si x = 0, borne unilatérale à 95 % 1 − 0,05^(1/R).",
         "L | n | R | garde non tenue | σ̂² = 0 | r_z | r_bloc | r_règle | discordances | NON ÉVALUABLE garde ; non "
         "qualifiable | SD(z) | SD(z_bloc) | FIV médian | run maximal de I ≥ ℓ"]
    for k in ent["cas"]:
        c, u, g = k["comptes"], k["taux"], k["diagnostics"]
        t.append(f"{k['L']} | {k['n']} | {c['R']} | {c['garde non tenue']} | {c['σ̂² = 0']} | {tx(u['z'])} | "
                 f"{tx(u['z_bloc'])} | {tx(u['regle'])} | {c['NE REJETTE PAS (discordance)']} | "
                 f"{c['NON ÉVALUABLE (garde §5.4)']} ; {c['NON ÉVALUABLE (rejet non qualifiable)']} | {f4(g['z_sd'])} | "
                 f"{f4(g['z_bloc_sd'])} | {f4(g['FIV_mediane'])} | {c['run maximal de I ≥ ℓ']}")
    for k in ent["cas"]:
        o = k["oracles"]
        t.append(f"Oracles L = {k['L']}, n = {k['n']} : (2) {o['(2) n²γ̂₀ = n·K(n − K)']} ; (2b) {o['(2b) N_lag = N_bloc']}"
                 " ; (5) " + " ; ".join(f"{e['controle']} : {e['moyenne']:.6f} contre {e['theorie']:.6f}, écart "
                                        f"{e['ecart_en_SE']:+.2f} SE" + (f" (limite n → ∞ : {e['limite_n_infini']:.6f})"
                                        if "limite_n_infini" in e else "") for e in o["(5)"])
                 + f" ; ρ^ℓ = {k['rho_puissance_ell']:.3e} ; empreinte {k['empreinte_sha256']}")
    return "\n".join(t) + "\n"


def sha256_fichier(chemin):
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description="SHOGEN-SIM-NIVEAU-1 (G0 du lot SIM-NIVEAU)")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--processus", type=int, default=1, help="paramètre d'exécution, écrit au .log.txt seulement")
    ap.add_argument("--R", type=int, default=R_DEFAUT)
    ap.add_argument("--p", type=float, default=P_DEFAUT)
    ap.add_argument("--cas", default="", help="L:n,L:n (essais seulement ; défaut : les 8 cas du G0)")
    a = ap.parse_args()
    cas = [tuple(map(int, x.split(":"))) for x in a.cas.split(",")] if a.cas else CAS
    noms = [os.path.join(a.sortie, "sim_niveau." + x) for x in ("json", "txt", "log.txt")]
    if any(map(os.path.exists, noms)):
        sys.exit("refus : un fichier de sortie existe deja (jamais d'ecrasement, G0 par. 6)")
    shas = {"sim_niveau.py": sha256_fichier(os.path.abspath(__file__)), "sim_niveau_calc.py": sha256_fichier(C.__file__)}
    debut, journal, tous, res = time.gmtime(), [], set(), []
    with (multiprocessing.Pool(a.processus) if a.processus > 1 else contextlib.nullcontext()) as pool:
        for L, n in cas:
            t0, taches = time.perf_counter(), ((a.p, L, n, r) for r in range(a.R))
            try:
                k, pids = agreger(a.p, L, n, a.R, pool.imap(C.tache, taches, 20) if pool else map(C.tache, taches))
            except RuntimeError as exc:
                sys.exit(f"ECHEC D'ORACLE, aucun fichier ecrit : {exc}")
            res.append(k)
            tous |= pids
            journal.append(f"cas L={L} n={n} : {time.perf_counter() - t0:.1f} s (horloge murale) ; PID distincts {len(pids)}")
            print(journal[-1], file=sys.stderr, flush=True)
    ent = {"schema": "shogen.sim-niveau.v1", "item": "SHOGEN-SIM-NIVEAU-1", "script_sha256": shas,
           "parametres": {"N": C.NSRC, "p": repr(a.p), "R": a.R, "cas": [list(x) for x in cas], "ell": C.ELL,
                          "seuil_z": str(C.SEUIL_Z), "comparaison": "≥, Decimal non arrondi", "garde_seuil": str(C.SEUIL_HIST),
                          "garde_blocs_n_min": C.N_MIN_BLOCS, "graine": C.GRAINE, "chaine_graine": C.CHAINE,
                          "chaine_effective_r0": C.CHAINE.format(g=C.GRAINE, p=a.p, L=cas[0][0], n=cas[0][1], r=0),
                          "derivation": "entier big-endian des 8 premiers octets de sha256(chaîne ASCII) -> random.Random ;"
                                        " 11·n appels à random() par réplication, flux i = 1..11 puis t = 1..n",
                          "decimal_prec": C.PREC},
           "alpha_nominal": 1 - NormalDist().cdf(2.33), "consequence_predeclaree": CONSEQUENCE, "cas": res}
    js, tx = json.dumps(ent, ensure_ascii=False, indent=1) + "\n", texte(ent)
    log = [f"script {os.path.abspath(__file__)} ; sha256 {shas}", f"python {sys.version} ; {sys.executable}",
           f"plateforme {platform.platform()} ; cpu_count {os.cpu_count()} ; processus {a.processus}",
           f"ligne de commande {sys.argv}", time.strftime("debut %Y-%m-%dT%H:%M:%SZ", debut)
           + time.strftime(" ; fin %Y-%m-%dT%H:%M:%SZ", time.gmtime()), *journal,
           f"PID distincts ayant servi des réplications, sur l'exécution : {len(tous)}",
           f"sha256 sim_niveau.json {hashlib.sha256(js.encode('utf-8')).hexdigest()}",
           f"sha256 sim_niveau.txt {hashlib.sha256(tx.encode('utf-8')).hexdigest()}"]
    os.makedirs(a.sortie, exist_ok=True)
    for nom, contenu in zip(noms, (js, tx, "\n".join(log) + "\n")):
        with open(nom, "xb") as f:
            f.write(contenu.encode("utf-8"))


if __name__ == "__main__":
    main()
