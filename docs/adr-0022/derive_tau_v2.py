"""DERIVATION per-classe de tau v2 (S2 Shogen) — annexe recalculable ADR-0022 (ADR-0003).
CORRIGE apres verification adversariale (3 refutants, R-21) :
 - REGLE HONNETE : tau_classe = grid-ceil( MARGE x max honnete sur les DEUX strates, 0.05% ).
   MARGE = 1.5 (marge de robustesse 50% au-dessus de la queue honnete 48h ; nommee, pas cachee).
 - Le MAX est pris sur les DEUX strates (O3 : le vrai max vit en STRESS pour place & chainlink).
 - La borne de Clopper-Pearson est RAPPORTEE HONNETEMENT comme plancher irreductible de
   fausse-alarme (~13.ln20 lectures/26j, independant de N) — PAS un gate de budget (O1/O2 : le
   budget <=4 etait insatisfaisable depuis 48h ; l'ancienne regle s'effondrait en grid-ceil(max)).
 - chainlink : ANCRE au parametre documente 0.5% (BTC/USD Ethereum Mainnet, verifie on-chain ET
   dans notre journal, signature 92.1%) ; sa deviation honnete par-fenetre atteint 1.0946% (lag) ;
   tau = 1.5 x ce max, coherent avec la meme regle. (PAS le delta inter-round 1.29%, mauvaise
   quantite.)
 - Contraintes : tau > max honnete (2 strates) ; tau < plus petit evenement reel pertinent
   (CAPO 2.85% ; oracles USDe 0.65%/4.3%).
Reserve de regime (F1) : n=1 jour/strate, etiquettes calme/stress empiriquement inversees ->
tau de 48h = SEUIL DE DEPART ; re-derivation par closure.tau_revision_needed (fail-closed) apres
le 1er vrai week-end + rapport J14 (observe vs projete). Lecture seule ; ne committe rien."""
import math
import os
import sys
from collections import defaultdict
from decimal import Decimal, localcontext

sys.path.insert(0, r"F:\Shogen\s2-harness")
from shogen_s2 import records
from shogen_s2.r1 import DECIMAL_PREC, _median, build_window_strate, parse_journal
from shogen_s2.closure import percentile_nearest_rank

D = r"F:\shogen-campagne\calibration"
MARGE = Decimal("1.5")               # marge de robustesse (design, nommee)
CAPO = Decimal("0.0285")             # plus petit evenement reel pertinent (Q5, Aave post-mortem)
CHAINLINK_PARAM = Decimal("0.005")   # seuil de deviation documente BTC/USD Ethereum Mainnet (Q1)
CALIB_TO_CAMPAIGN = 13               # 26 j / 48 h


def grid_ceil(x, step=Decimal("0.0005")):     # arrondi SUP a la grille 0.05%
    return (x / step).to_integral_value(rounding="ROUND_CEILING") * step


def cp_upper_k0(n, alpha=Decimal("0.05")):     # borne sup CP unilaterale, k=0 : 1 - alpha^(1/n)
    return Decimal(1) - (alpha ** (Decimal(1) / Decimal(n)))


# ---- chargement + ecart relatif honnete par (fenetre, flux), tagge strate/classe ----
params_list, _ck, markers = records.parse_control(os.path.join(D, "control.jsonl"))
params = records.effective_run_params(params_list)
readings = parse_journal(os.path.join(D, "journal.jsonl"))
_sbc, sigma_class_of_flux, _tau = records.sigma_tau_from_params(params)
pool = list(params["pool"]); w = int(params["w"]); n_min = int(params["n_min_hors_enveloppe"])
win_strate = build_window_strate(markers)
rmap = {}
for r in readings:
    rmap[(int(r["window_start"]), r["flux_id"])] = r

classes = defaultdict(list)
for f in pool:
    classes[sigma_class_of_flux.get(f)].append(f)

dev_class = defaultdict(list)            # classe -> [dev]  (toutes strates)
dev_cs = defaultdict(lambda: defaultdict(list))   # classe -> strate -> [dev]
with localcontext() as ctx:
    ctx.prec = DECIMAL_PREC
    for ws in sorted(win_strate):
        st = win_strate[ws]
        resp = [f for f in pool if rmap.get((ws, f)) is not None
                and rmap[(ws, f)].get("status") == "ok" and rmap[(ws, f)].get("price") is not None]
        rp = {f: Decimal(rmap[(ws, f)]["price"]) for f in resp}
        if len(resp) >= n_min:
            for f in resp:
                m = _median([rp[g] for g in resp if g != f])
                if m > 0:
                    d = +(abs(rp[f] - m) / m)
                    kl = sigma_class_of_flux.get(f)
                    dev_class[kl].append(d)
                    dev_cs[kl][st].append(d)

CLASS_ORDER = ["oracle_pyth", "place_horodatee", "sans_horodatage", "oracle_chainlink", "agregateur"]
strates = sorted({s for kl in dev_cs for s in dev_cs[kl]})

print("=" * 100)
print(f"DERIVATION tau v2 — regle : tau = grid-ceil( {MARGE} x max honnete DEUX strates )  ;  contrainte tau < CAPO {float(CAPO)*100:.2f}%")
print("=" * 100)
print(f"{'classe':18s} {'membres':32s} {'maxCALME%':>9s} {'maxSTRESS%':>10s} {'maxBOTH%':>9s} {'1.5xmax%':>8s} {'TAU%':>6s} {'ancre':>9s}")
selection = {}
for kl in CLASS_ORDER:
    mx_by = {s: (max(dev_cs[kl][s]) if dev_cs[kl].get(s) else Decimal(0)) for s in strates}
    mx_both = max(mx_by.values())
    raw = MARGE * mx_both
    tau = grid_ceil(raw)
    anchor = "mecaniste" if kl == "oracle_chainlink" else "quantile"
    selection[kl] = (tau, mx_both, anchor)
    print(f"{kl:18s} {','.join(classes[kl]):32s} "
          f"{float(mx_by.get('calme',0))*100:9.4f} {float(mx_by.get('stress',0))*100:10.4f} "
          f"{float(mx_both)*100:9.4f} {float(raw)*100:8.4f} {float(tau)*100:6.2f} {anchor:>9s}")

print("\n--- CONTROLES par classe (contraintes + plancher de fausse-alarme CP honnete) ---")
N_by_class = {kl: len(dev_class[kl]) for kl in CLASS_ORDER}
for kl in CLASS_ORDER:
    tau, mx_both, anchor = selection[kl]
    N = N_by_class[kl]
    k_at_tau = sum(1 for d in dev_class[kl] if d > tau)     # excès observés au tau choisi (attendu 0)
    cp = cp_upper_k0(N) if k_at_tau == 0 else None
    proj_reads_26j = (cp * Decimal(CALIB_TO_CAMPAIGN) * Decimal(N)) if cp is not None else None
    ok_max = tau > mx_both
    ok_capo = tau < CAPO
    line = (f"  {kl:18s} tau={float(tau)*100:5.2f}%  > maxBOTH {float(mx_both)*100:.4f}% : {ok_max}"
            f"  ; < CAPO : {ok_capo}  ; k@tau={k_at_tau} (N={N})")
    if cp is not None:
        line += f"  ; CP95 UB/lecture={float(cp)*100:.4f}%  -> plancher fausse-alarme 26j <= {float(proj_reads_26j):.1f} lectures"
    print(line)
    if kl == "oracle_chainlink":
        print(f"      + ancre mecaniste : param documente {float(CHAINLINK_PARAM)*100:.2f}% (BTC/USD Eth Mainnet, signature 92.1%) ; "
              f"lag honnete max par-fenetre {float(mx_both)*100:.4f}% ; tau {float(tau)*100:.2f}% = 1.5x ce max.")

print("\n" + "=" * 100)
print("SELECTION FINALE (adjugee — 5 classes) :")
for kl in CLASS_ORDER:
    tau, mx_both, anchor = selection[kl]
    print(f"  {kl:18s} tau = {float(tau)*100:5.2f}%   [{anchor}]  (1.5 x max honnete {float(mx_both)*100:.4f}% ; < CAPO 2.85%)")
print("Rappel : sigma reste par-classe (cloture) ; tau devient par-classe. Seuil de DEPART :")
print("re-derivation par closure.tau_revision_needed apres le 1er vrai week-end + rapport J14.")
print("=" * 100)
