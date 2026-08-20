"""Table de sortie §6 — recalculable offline (ADR-0003). Étendue par M1b.

Conception : docs/10-mesures-pilotes-design.md §6 (« tout chiffre du rapport se
recalcule depuis le journal par un lecteur sans accès à Shōgen », ADR-0003).

Six blocs (§6). M1b calcule 1–4 ; **5–6 différés à M1c** (requièrent R2) :
  1. **Paramètres** — depuis `run_params` : pool, w, seuils, précision, version,
     dates, calendrier de strates committé, contrôle d'horloge, **composition de
     devise du pool** (§2, devise marquée) + résidu de peg nommé (→ R2(2a), M1c).
  2. **Journal brut** — par fenêtre×source : valeur, devise, horodatage porté,
     statut d'écart, sha256 des octets bruts (ADR-0005 : hash toujours).
  3. **R1** — p̂ᵢ, n, K par strate, P̂₀/P̂₁/P̂_more, z **ou** la **queue binomiale
     exacte** sous la garde (§5.4) **ou** « historique insuffisant » nu (dégénéré),
     comptes non évaluables, A(window-stationarity).
  4. **L&M** — Ê(Θ), Ê(Θ²), Var̂(Θ) par strate, corrélations φ **signées** par
     paire de flux ; renvois M1c nommés (clusters, agrégation flux→source).
  5. **R2** — DIFFÉRÉ M1c (VIDE) : ASN/contenu/méthode, k_eff, les 7 résidus.
  6. **Tête de certificat** — DIFFÉRÉ M1c (VIDE) : k_eff, k nominal, DRAPEAU 2
     « co-défaillance non expliquée par R2 » (§5.6). Seul le drapeau « historique
     insuffisant » (§5.4) est calculé ici (bloc 3).

`render_report` ne lit QUE les fichiers de journal → recalculable par un tiers.
Sortie **déterministe** (mêmes fichiers → même texte) : répétition générale du
claim de recalculabilité (plan §5).
"""

from __future__ import annotations

import os
import sys
from decimal import Decimal

from . import records
from .lm import compute_lm
from .r1 import (
    A_WINDOW_STATIONARITY,
    classify_cells,
    compute_r1,
    parse_journal,
)
from .window import verify_markers_against_spec


def _fmt_dec(x) -> str:
    """Decimal → chaîne exacte (recalculable) ; None → tiret."""
    return "-" if x is None else str(x)


def render_report(control_path: str, journal_path: str) -> str:
    params_list, clock_checks, markers = records.parse_control(control_path)
    # Concordance des run_params successifs (fail-closed, §E) — même garde que
    # l'oracle : une table depuis des seuils divergents serait un mensonge.
    params = records.effective_run_params(params_list)
    # Strates journalées == calendrier committé (fail-closed, §5.3) — même garde
    # que l'oracle : une table sur des strates trafiquées serait un mensonge. Clés
    # porteuses PRÉSENTES (garanties par effective_run_params), lues sans défaut.
    div = verify_markers_against_spec(markers, params["strate_calendar"])
    if div:
        raise ValueError(
            f"strates journalées incohérentes avec le calendrier committé (§5.3) : {div[:5]}"
        )
    readings = parse_journal(journal_path)
    pool = list(params["pool"])
    w = int(params["w"])
    sigma = Decimal(str(params["sigma_classe"]))
    tau = Decimal(str(params["tau_classe"]))
    seuil_hist = Decimal(str(params["seuil_historique_valeur"]))
    n_min = int(params["n_min_hors_enveloppe"])

    r1 = compute_r1(markers, readings, pool, w, sigma, tau, seuil_hist, n_min)
    cells = classify_cells(markers, readings, pool, w, sigma, tau, n_min)
    reading_map = {(int(r["window_start"]), r["flux_id"]): r for r in readings}

    out: list[str] = []
    ap = out.append

    # ── Bloc 1 : Paramètres ────────────────────────────────────────────────
    ap("=" * 78)
    ap("TABLE §6 (S2 Phase A — M1b) — recalculable depuis le journal seul (ADR-0003)")
    ap("=" * 78)
    ap("\n[BLOC 1] PARAMÈTRES")
    for key in ("harness_version", "classe", "pool", "w", "sample_lead",
                "sigma_classe", "tau_classe", "kappa", "seuil_historique_valeur",
                "n_min_hors_enveloppe", "strate_defaut", "decimal_prec",
                "seuil_historique", "seuil_z", "residu_staleness",
                "n_windows_demande", "started_utc", "note_skeleton"):
        if key in params:
            ap(f"  {key:24} = {params[key]}")
    ap(f"  {'run_params_demarrages':24} = {len(params_list)} (concordants sur les "
       f"champs porteurs — §E)")
    if "strate_calendar" in params:
        sc = params["strate_calendar"]
        ap(f"  {'strate_calendar':24} = kind={sc.get('kind')} "
           f"{sc.get('note', '')}".rstrip())
    # Devise MARQUÉE par flux (§2, décision 4) : composition du pool + résidu peg
    # nommé (le démêlage USDT/USD est R2(2a), DIFFÉRÉ M1c — jamais calculé ici).
    cur_by_flux: dict = {}
    for r in readings:
        c = r.get("currency")
        if c is not None:
            cur_by_flux.setdefault(r["flux_id"], c)
    n_usd = sum(1 for c in cur_by_flux.values() if c == "USD")
    n_usdt = sum(1 for c in cur_by_flux.values() if c == "USDT")
    ap(f"  {'devise_composition':24} = {n_usd} USD / {n_usdt} USDT (classe "
       f"« BTC/USD-stable », devise marquée par flux — 10 §2/§9.4)")
    ap(f"  {'residu_peg_usdt_usd':24} = écart de peg USDT/USD = résidu R2(2a) "
       f"(ρ_resid) — DIFFÉRÉ M1c, nommé jamais calculé ici (10 §2/§9.4)")
    for cc in clock_checks:
        ap(f"  {'controle_horloge':24} = phase={cc['phase']} médiane_offset(s)="
           f"{_fmt_dec(cc['median_offset'])} "
           f"sources={list(cc['offsets'])} {cc['note'] or ''}".rstrip())

    # ── Bloc 2 : Journal brut ──────────────────────────────────────────────
    ap("\n[BLOC 2] JOURNAL BRUT (par fenêtre × source)")
    hdr = (f"  {'window_start':>12} {'flux':10} {'cur':4} {'statut_ecart':16} "
           f"{'price':>16} {'source_ts':>18} {'sha256[:12]'}")
    ap(hdr)
    ap("  " + "-" * (len(hdr) - 2))
    for (ws, flux) in sorted(cells):
        rd = reading_map.get((ws, flux), {})
        cur = rd.get("currency") or "-"
        price = rd.get("price") or "-"
        src = rd.get("source_ts")
        src_s = _fmt_dec(src)
        sha = (rd.get("sha256_raw") or "-")[:12]
        ap(f"  {ws:>12} {flux:10} {cur:4} {cells[(ws, flux)].value:16} "
           f"{price:>16} {src_s:>18} {sha}")

    # ── Bloc 3 : R1 ────────────────────────────────────────────────────────
    ap("\n[BLOC 3] R1 (test K&L §5 transposé — 10 §5.1/§5.2/§5.4)")
    if r1.get("note"):
        ap(f"  {r1['note']}")
        ap(f"  drapeau « historique insuffisant » = {r1['flag_historique_insuffisant']}")
    for st, blk in r1.get("strates", {}).items():
        ap(f"\n  ── strate « {st} » : n = {blk['n']} fenêtres complétées ; "
           f"K = {blk['K']} (fenêtres à ≥ 2 écarts)")
        ph = (f"    {'source':10} {'p̂ᵢ':>26} {'écart':>6} "
              f"{'panne':>6} {'stale':>6} {'horsE':>6} {'nonÉv':>6} "
              f"{'axes évaluables'}")
        ap(ph)
        for f in pool:
            s = blk["per_source"][f]
            ap(f"    {f:10} {_fmt_dec(s['phat']):>26} {s['ecart']:>6} "
               f"{s['panne']:>6} {s['staleness']:>6} {s['hors_enveloppe']:>6} "
               f"{s['non_eval_hors_env']:>6} {','.join(s['axes_evaluables'])}")
        residu = blk.get("residu_staleness_fail_open", [])
        if residu:
            ap(f"    résidu staleness fail-open (répond sans horodatage porté, (ii) "
               f"non évaluable) : {','.join(residu)} (§G ; 03 §1)")
        ap(f"    P̂₀      = {_fmt_dec(blk['P0'])}")
        ap(f"    P̂₁      = {_fmt_dec(blk['P1'])}")
        ap(f"    P̂_more  = {_fmt_dec(blk['P_more'])}")
        ap(f"    n·P̂_more·(1−P̂_more) = {_fmt_dec(blk['gate_value'])} "
           f"(seuil {_fmt_dec(blk['seuil_historique'])})")
        if blk["flag_historique_insuffisant"]:
            ap("    z       = non publié (garde §5.4 : n·P̂_more·(1−P̂_more) < 10) — "
               "aucun z non significatif présenté comme absence de dépendance (04 §2)")
            if blk.get("queue_exacte_applicable"):
                ap(f"    queue exacte P(K ≥ K_obs={blk['K']} | Bin(n={blk['n']}, P̂_more)) "
                   f"= {_fmt_dec(blk['queue_binomiale_P_K_ge_Kobs'])} "
                   f"({blk.get('queue_note', '')})")
            else:
                ap(f"    HISTORIQUE INSUFFISANT — queue {blk.get('queue_note', '')}")
        else:
            ap(f"    z       = {_fmt_dec(blk['z'])} (seuil {_fmt_dec(blk['seuil_z'])}, "
               f"unilatéral — 10 §5.1)")
    ap(f"\n  {A_WINDOW_STATIONARITY}")

    # ── Bloc 4 : L&M (§5.5) ────────────────────────────────────────────────
    lm_out = compute_lm(markers, readings, pool, w, sigma, tau, n_min)
    ap(f"\n[BLOC 4] L&M (§5.5) — fonction de difficulté Θ ; N = {lm_out['N']} flux (pool)")
    for st, blk in lm_out["strates"].items():
        ap(f"\n  ── strate « {st} » : n = {blk['n']} ; Σ mⱼ = {blk['sum_m']}")
        ap(f"    Ê(Θ)    = {_fmt_dec(blk['E_theta'])}  (= (1/N)·Σᵢ p̂ᵢ — cohérence R1)")
        ap(f"    Ê(Θ²)   = {_fmt_dec(blk['E_theta2'])}  (forme par paires mⱼ(mⱼ−1)/(N(N−1)))")
        ap(f"    Var̂(Θ)  = {_fmt_dec(blk['Var_theta'])}  (= Ê(Θ²) − Ê(Θ)² ; écart au "
           "modèle d'indépendance, L&M éq.16 ; Cov<0 possible)")
        pair_items = list(blk["pair_phi"].items())
        n_defined = sum(1 for _, v in pair_items if v["phi"] is not None)
        n_none = len(pair_items) - n_defined
        n_coecart = sum(1 for _, v in pair_items if v["n11"] > 0)
        ap(f"    corrélations φ signées (indicatrices d'écart) : {n_defined} définies, "
           f"{n_none} non définies (indicatrice constante) / {len(pair_items)} paires de "
           f"flux ; {n_coecart} paires à co-écart (n11>0)")
        # Matrice de co-écarts COMPLÈTE (10 §6 bloc 4, l.544) : TOUTES les paires,
        # y compris φ=None (indicatrice constante — ex. une source en panne partout,
        # le co-écart le plus extrême) et φ=0. Sa CONSOMMATION par le DRAPEAU 2
        # (§5.6) est DIFFÉRÉE M1c ; la donnée (n11..n00 sur 66 paires) est livrée ici.
        ap("    matrice de co-écarts COMPLÈTE (§6 bloc 4 ; consommation drapeau 2 §5.6 "
           "différée M1c) — par paire [n11 n10 n01 n00] φ (co-écarts en tête) :")
        for k, v in sorted(pair_items, key=lambda kv: (-kv[1]["n11"], kv[0])):
            phi_s = _fmt_dec(v["phi"]) if v["phi"] is not None else "non_définie"
            ap(f"      {k:26} [{v['n11']} {v['n10']} {v['n01']} {v['n00']}] "
               f"φ={phi_s} ({v['signe']})")
        ap(f"    renvoi M1c : {blk['renvoi_m1c_clusters']}")
        ap(f"    renvoi M1c : {blk['renvoi_m1c_flux_source']}")
        ap(f"    caveat : {blk['caveat_non_eval']}")

    # ── Bloc 5 : R2 — DIFFÉRÉ M1c ──────────────────────────────────────────
    ap("\n[BLOC 5] R2 (ASN / contenu / méthode) — DIFFÉRÉ À M1c : VIDE cette passe")
    ap("  axes §4.1–§4.3 (ASN croisé, ρ_raw/ρ_resid/T/(K,z)/δ par paire, arêtes "
       "basis:doc|measured ADR-0008), k_eff côté livraison, les 7 résidus — hors "
       "périmètre M1b (requièrent la collecte R2, non faite ici).")

    # ── Bloc 6 : Tête de certificat — DIFFÉRÉ M1c ──────────────────────────
    ap("\n[BLOC 6] TÊTE DE CERTIFICAT — DIFFÉRÉ À M1c : VIDE cette passe")
    ap("  k_eff, k nominal, partition R2 nommée, et le DRAPEAU 2 « co-défaillance "
       "observée non expliquée par les axes R2 » (§5.6) requièrent R2 (M1c). Seul "
       "le drapeau « historique insuffisant » (§5.4) est calculé ici (bloc 3).")
    ap("=" * 78)
    return "\n".join(out)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m shogen_s2.report <journal_dir>", file=sys.stderr)
        return 2
    d = argv[1]
    text = render_report(os.path.join(d, "control.jsonl"),
                         os.path.join(d, "journal.jsonl"))
    # Émission UTF-8 explicite : la table porte la notation de doc 10 (P̂₀, p̂ᵢ…)
    # dont des diacritiques combinants qu'une console cp1252 (Windows) ne peut
    # encoder ; l'artefact recalculable est UTF-8, indépendant du code-page.
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
