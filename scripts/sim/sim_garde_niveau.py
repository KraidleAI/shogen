"""SHOGEN-CRITERE-GARDE-NIVEAU-1 (partie 3 de S2, étape S), sous-lot S-a : niveau de z_s seul et de la règle
SHOGEN-CRITERE-R1-1 près de la garde §5.4 (n·P̂(1 − P̂) de 10 à 30, n ≥ 30·ℓ) sous le modèle nul synthétique de
SIM-NIVEAU (ADR-0028 §1 bis.1 pts 2, 3, 5, 7, 11 ; annexe B l.305). Cas, R, graine, définitions, lecture : journal G1
docs/G1-partie-3-S.md §1 et §2, écrits avant toute exécution. Réplication : sim_niveau_calc.replication ; agrégation :
sim_niveau.agreger (oracles (2), (2b), (5), empreinte) ; tous deux inchangés, aucune ligne de la règle recopiée ici.
Ajouts : distribution des valeurs, taux conditionnels à la garde tenue, classes de la garde imprimée, écarts à 0,01 en
erreurs-types, référence binomiale exacte à P connu (hors règle), indices des REJETTE, empreinte des R/20 premiers
enregistrements. Fail-closed (sortie ≠ 0, aucun fichier, jamais d'écrasement). Oracle : sim_garde_niveau_oracle_r1.py.
Usage : python3.13 -B sim_garde_niveau.py --sortie DOSSIER [--processus k] [--diviseur d]  (worker G1 claude-opus-5-5, 2026-10-02)"""
import argparse, contextlib, hashlib, json, math, multiprocessing, os, platform, sys, time
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from statistics import NormalDist

import sim_niveau as S
import sim_niveau_calc as C

R_I, R_D, DIV_PREFIXE, SEUIL_LECTURE = 30000, 6000, 20, 0.01           # journal §2, §1.7, §1.8
GRILLE = ((7200, "0.005107", 10), (7200, "0.006279", 15), (7200, "0.007274", 20), (7200, "0.00896", 30),
          (25000, "0.00272", 10), (25000, "0.003338", 15), (25000, "0.00386", 20), (25000, "0.004741", 30))
CAS = ([(1, n, p, g, R_I) for n, p, g in GRILLE]                       # journal §1.3 : L, puis n, puis g
       + [(L, n, p, g, R_D) for L in (5, 20, 60) for n, p, g in GRILLE if g in (10, 30)])
CLASSES = (("[10 ; 12,5)", Decimal("12.5")), ("[12,5 ; 15)", Decimal(15)), ("[15 ; 20)", Decimal(20)),
           ("[20 ; 30)", Decimal(30)), ("[30 ; +∞)", None))           # garde tenue : ĝ ≥ 10 (journal §1.6)
V = S.VALEURS
CONSEQUENCE = ("Conséquence pré-déclarée (G0 de la partie 3, section S ; ADR-0028 §1 bis.1 pt 7, même principe) : cette "
               "sortie ne modifie ni ℓ, ni le seuil, ni la règle ; elle est imprimée au paquet avec ses erreurs-types ; "
               "un niveau mesuré au-dessus de 0,01 devient une limite écrite au paquet, jamais une révision. Ni les cas, "
               "ni R, ni la graine, ni les définitions des taux ne changent après la lecture d'une sortie (journal G1, "
               "§1). Niveau sous un modèle nul synthétique : rien n'est établi sur des sources réelles (doc 09).")


def pmore(p):
    """P_more(p) exact, N_FLUX flux de même p (Fraction du flottant simulé, comme sim_niveau.agreger)."""
    pf = Fraction(float(p))
    return 1 - (1 - pf) ** S.N_FLUX - S.N_FLUX * pf * (1 - pf) ** (S.N_FLUX - 1)


def reference(n, p):
    """Hors règle (journal §1.6) : k* = min{k : sim_niveau_calc.z_score(n, k, P) ≥ 2,33}, P = P_more(p) connu ;
    P(K ≥ k*) pour K ~ Bin(n, P) = 1 − Σ_{k<k*} pmf(k), pmf par récurrence, Decimal à la précision de C.PREC."""
    P = pmore(p)
    with localcontext() as ctx:
        ctx.prec = C.PREC
        Pd, k = Decimal(P.numerator) / Decimal(P.denominator), math.ceil(n * P)
        while C.z_score(n, k, Pd) < C.SEUIL_Z:
            k += 1
        pmf, cum = (1 - Pd) ** n, Decimal(0)
        for j in range(k):
            cum, pmf = cum + pmf, pmf * (n - j) / (j + 1) * Pd / (1 - Pd)
        return {"P_more": str(Pd), "k_etoile": k, "niveau": str(+(1 - cum))}


def suivre(recs, x, R):
    """Accumule dans x, dans l'ordre des r, les ajouts du journal (§1.6, §1.7) ; rend chaque enregistrement à agreger."""
    h = hashlib.sha256()
    for r, d in enumerate(recs):
        v = d["valeur"]
        if d["tenue"]:
            i, g = next(i for i, (_, b) in enumerate(CLASSES) if b is None or d["garde"] < b), d["garde"]
            y, e = x["classes"][i], x["bornes"][i]
            e[:] = [g, g] if y["m"] == 0 else [min(e[0], g), max(e[1], g)]
            y["m"] += 1
            y["z"] += d["z"] >= C.SEUIL_Z
            y[v] += 1
        if v in (V[0], V[4]) or (v == V[2] and len(x[V[2]]) < 50):
            x[v].append(r)
        if r < R // DIV_PREFIXE:
            h.update(d["ligne"].encode("utf-8"))
        yield d
    x["prefixe"] = h.hexdigest()


def completer(k, p, g, x):
    """Ajoute au cas rendu par agreger les champs du journal §1.6 à §1.8, depuis ses comptes et ceux de x."""
    c, R, P = k["comptes"], k["comptes"]["R"], pmore(p)
    t = R - c["garde non tenue"]
    ct = {"z": S.taux(c["z ≥ 2,33"], t), "regle": S.taux(c[V[0]], t)} if t else {"z": None, "regle": None}
    ec = lambda u: None if u is None or u["SE"] == 0 else (u["r"] - SEUIL_LECTURE) / u["SE"]
    k.update({"p": p, "g_cible": g, "g_theorique": float(k["n"] * P * (1 - P)),
              "valeurs": {v: S.taux(c[v], R) for v in V},
              "valeurs_pt5": {"REJETTE": S.taux(c[V[0]], R), "NE REJETTE PAS": S.taux(c[V[1]] + c[V[2]], R),
                              "NON ÉVALUABLE": S.taux(c[V[3]] + c[V[4]], R)},
              "garde_tenue": t, "conditionnels_garde_tenue": ct,
              "lecture": {"r_z": ec(k["taux"]["z"]), "r_z_t": ec(ct["z"]), "r_regle": ec(k["taux"]["regle"]),
                          "r_regle_t": ec(ct["regle"])},
              "classes_garde": [{"classe": nom, "m": y["m"], "g_min_max": list(map(str, e)),
                                 **({w: S.taux(y[w], y["m"]) for w in ("z", V[0], V[2], V[4])} if y["m"] else {})}
                                for (nom, _), y, e in zip(CLASSES, x["classes"], x["bornes"])],
              "reference_iid_P_connu": reference(k["n"], p),
              "indices": {"REJETTE": x[V[0]], "discordance_50_premieres": x[V[2]], "rejet_non_qualifiable": x[V[4]]},
              "prefixe_R": R // DIV_PREFIXE, "empreinte_prefixe": x["prefixe"]})
    return k


def fx(u):
    """Taux imprimé : x → r (SE), borne à 95 % si x = 0 ; « — » si le dénominateur est nul."""
    return "—" if u is None else (f"{u['x']} → {u['r']:.5f} (SE {u['SE']:.5f})"
                                  + (f" [borne 95 % {u['borne95_si_x_nul']:.2e}]" if u["x"] == 0 else ""))


def texte(ent):
    """Sortie texte : en-tête, une ligne par cas, classes de garde, oracles ; ni heure ni durée (bit-identité)."""
    P, e2, f4 = ent["parametres"], (lambda v: "—" if v is None else f"{v:+.2f}"), (lambda v: "—" if v is None else f"{v:.4f}")
    t = ["SHOGEN-CRITERE-GARDE-NIVEAU-1 (" + ent["schema"] + ") ; " + " ; ".join(f"{k} sha256 {v}" for k, v in
                                                                                ent["script_sha256"].items()),
         f"Modèle nul et code de SIM-NIVEAU, inchangés (sim_niveau_calc.replication, sim_niveau.agreger) : N = {P['N']} "
         f"flux simulés, mutuellement indépendants par construction ; ℓ = {P['ell']} ; REJETTE ⇔ z ≥ {P['seuil_z']} ∧ "
         f"z_bloc ≥ {P['seuil_z']} ; garde tenue ⇔ n·P̂(1−P̂) ≥ {P['garde_seuil']} ; z_bloc publiée ⇔ σ̂² > 0 ∧ n ≥ "
         f"{P['garde_blocs_n_min']} ; graine {P['graine']}, chaîne {P['chaine_graine']} (r = 0 du premier cas : "
         f"{P['chaine_effective_r0']}) ; Decimal, précision {P['decimal_prec']} ; R = R0/{P['diviseur']} par cas, "
         f"R0 = {R_I} (L = 1) et {R_D} (L > 1).",
         f"α nominal = 1 − Φ(2,33) = {ent['alpha_nominal']:.8f}, pour comparaison ; seuil de lecture 0,01.",
         ent["consequence_predeclaree"],
         "Taux : r_z = #{garde tenue ∧ z ≥ 2,33}/R ; r_z|t = même compte/#{garde tenue} ; r_règle = #{REJETTE}/R ; "
         "r_règle|t = #{REJETTE}/#{garde tenue} ; r_bloc = #{z_bloc publiée ∧ z_bloc ≥ 2,33}/R ; SE = √(r(1−r)/D) ; "
         "si x = 0, borne 1 − 0,05^(1/D) ; [e] = (r − 0,01)/SE. Référence hors règle : P(K ≥ k*), K ~ Bin(n, P_more(p)), "
         "P connu, fenêtres iid.",
         "L | n | p | g cible (théorique) | R | garde non tenue | σ̂² = 0 | r_z [e] | r_z|t [e] | r_règle [e] | "
         "r_règle|t [e] | r_bloc | NE REJETTE PAS : z < 2,33 ; discordance | NON ÉVALUABLE : garde ; non qualifiable | "
         "référence : k* ; niveau | SD(z) | FIV médian | run maximal de I ≥ ℓ"]
    for k in ent["cas"]:
        c, u, ct, le, rf = (k["comptes"], k["taux"], k["conditionnels_garde_tenue"], k["lecture"],
                            k["reference_iid_P_connu"])
        t.append(f"{k['L']} | {k['n']} | {k['p']} | {k['g_cible']} ({k['g_theorique']:.4f}) | {c['R']} | "
                 f"{c['garde non tenue']} | {c['σ̂² = 0']} | {fx(u['z'])} [{e2(le['r_z'])}] | {fx(ct['z'])} "
                 f"[{e2(le['r_z_t'])}] | {fx(u['regle'])} [{e2(le['r_regle'])}] | {fx(ct['regle'])} "
                 f"[{e2(le['r_regle_t'])}] | {fx(u['z_bloc'])} | {c[V[1]]} ; {c[V[2]]} | {c[V[3]]} ; {c[V[4]]} | "
                 f"{rf['k_etoile']} ; {float(Decimal(rf['niveau'])):.6f} | {f4(k['diagnostics']['z_sd'])} | "
                 f"{f4(k['diagnostics']['FIV_mediane'])} | {c['run maximal de I ≥ ℓ']}")
    t.append("Classes de la garde imprimée ĝ (garde tenue) — classe : m ; puis, sur m : z ≥ 2,33 ; REJETTE ; "
             "discordance ; rejet non qualifiable")
    for k in ent["cas"]:
        t.append(f"L = {k['L']}, n = {k['n']}, p = {k['p']} : " + " | ".join(
            f"{y['classe']} : {y['m']}" + (" ; " + " ; ".join(fx(y[w]) for w in ("z", V[0], V[2], V[4])) if y["m"] else "")
            for y in k["classes_garde"]))
    for k in ent["cas"]:
        o = k["oracles"]
        t.append(f"Oracles L = {k['L']}, n = {k['n']}, p = {k['p']} : (2) {o['(2) n²γ̂₀ = n·K(n − K)']} ; (2b) "
                 f"{o['(2b) N_lag = N_bloc']} ; (5) " + " ; ".join(f"{e['controle']} : écart {e['ecart_en_SE']:+.2f} SE"
                                                                  for e in o["(5)"])
                 + f" ; ρ^ℓ = {k['rho_puissance_ell']:.3e} ; empreinte {k['empreinte_sha256']} ; empreinte des "
                 f"{k['prefixe_R']} premiers {k['empreinte_prefixe']}")
    return "\n".join(t) + "\n"


def main():
    ap = argparse.ArgumentParser(description="SHOGEN-CRITERE-GARDE-NIVEAU-1 (journal G1 docs/G1-partie-3-S.md)")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--processus", type=int, default=1, help="paramètre d'exécution, écrit au .log.txt seulement")
    ap.add_argument("--diviseur", type=int, default=1, help="R = R0/d par cas : bit-identité (journal §1.7), essais")
    a = ap.parse_args()
    noms = [os.path.join(a.sortie, "garde_niveau." + x) for x in ("json", "txt", "log.txt")]
    if any(map(os.path.exists, noms)):
        sys.exit("refus : un fichier de sortie existe deja (jamais d'ecrasement)")
    shas = {os.path.basename(f): S.sha256_fichier(f) for f in (os.path.abspath(__file__), S.__file__, C.__file__)}
    debut, journal, tous, res = time.gmtime(), [], set(), []
    with (multiprocessing.Pool(a.processus) if a.processus > 1 else contextlib.nullcontext()) as pool:
        for L, n, p, g, R0 in CAS:
            R, x = R0 // a.diviseur, {"classes": [Counter() for _ in CLASSES], "bornes": [[] for _ in CLASSES],
                                      V[0]: [], V[2]: [], V[4]: []}
            t0, taches = time.perf_counter(), ((float(p), L, n, r) for r in range(R))
            recs = pool.imap(C.tache, taches, 20) if pool else map(C.tache, taches)
            try:
                k, pids = S.agreger(float(p), L, n, R, suivre(recs, x, R))
            except RuntimeError as exc:
                sys.exit(f"ECHEC D'ORACLE, aucun fichier ecrit : {exc}")
            res.append(completer(k, p, g, x))
            tous |= pids
            journal.append(f"cas L={L} n={n} p={p} R={R} : {time.perf_counter() - t0:.1f} s (horloge murale) ; "
                           f"PID distincts {len(pids)}")
            print(journal[-1], file=sys.stderr, flush=True)
    ent = {"schema": "shogen.sim-garde-niveau.v1", "item": "SHOGEN-CRITERE-GARDE-NIVEAU-1", "script_sha256": shas,
           "journal": "docs/G1-partie-3-S.md, §1 et §2 (pré-enregistrement)",
           "parametres": {"N": C.NSRC, "cas": [list(x) for x in CAS], "diviseur": a.diviseur, "ell": C.ELL,
                          "seuil_z": str(C.SEUIL_Z), "comparaison": "≥, Decimal non arrondi",
                          "garde_seuil": str(C.SEUIL_HIST), "garde_blocs_n_min": C.N_MIN_BLOCS, "graine": C.GRAINE,
                          "chaine_graine": C.CHAINE, "chaine_effective_r0": C.CHAINE.format(
                              g=C.GRAINE, p=float(CAS[0][2]), L=CAS[0][0], n=CAS[0][1], r=0),
                          "decimal_prec": C.PREC, "classes_garde": [nom for nom, _ in CLASSES],
                          "prefixe": f"R/{DIV_PREFIXE}", "seuil_lecture": str(SEUIL_LECTURE)},
           "alpha_nominal": 1 - NormalDist().cdf(2.33), "consequence_predeclaree": CONSEQUENCE, "cas": res}
    js, tx = json.dumps(ent, ensure_ascii=False, indent=1) + "\n", texte(ent)
    log = [f"script {os.path.abspath(__file__)} ; sha256 {shas}", f"python {sys.version} ; {sys.executable}",
           f"plateforme {platform.platform()} ; cpu_count {os.cpu_count()} ; processus {a.processus}",
           f"ligne de commande {sys.argv}", time.strftime("debut %Y-%m-%dT%H:%M:%SZ", debut)
           + time.strftime(" ; fin %Y-%m-%dT%H:%M:%SZ", time.gmtime()), *journal,
           f"PID distincts ayant servi des réplications, sur l'exécution : {len(tous)}",
           f"sha256 garde_niveau.json {hashlib.sha256(js.encode('utf-8')).hexdigest()}",
           f"sha256 garde_niveau.txt {hashlib.sha256(tx.encode('utf-8')).hexdigest()}"]
    os.makedirs(a.sortie, exist_ok=True)
    for nom, contenu in zip(noms, (js, tx, "\n".join(log) + "\n")):
        with open(nom, "xb") as f:
            f.write(contenu.encode("utf-8"))


if __name__ == "__main__":
    main()
