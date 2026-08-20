"""Table de sortie §6 — **minimale** (walking skeleton), recalculable offline.

Conception : docs/10-mesures-pilotes-design.md §6 (« tout chiffre du rapport se
recalcule depuis le journal par un lecteur sans accès à Shōgen », ADR-0003).
Plan S2 §3 (table §6 minimale : Paramètres + Journal brut + bloc R1).

Trois blocs (les six blocs complets — L&M, R2, tête de certificat — viennent
avec le harnais complet, hors périmètre skeleton) :
  1. **Paramètres** — depuis `run_params` (dans le journal) : pool, w, seuils,
     précision, version, dates, contrôle d'horloge consigné.
  2. **Journal brut** — par fenêtre×source : valeur, devise, horodatage porté,
     statut d'écart (ok / panne / staleness / hors-enveloppe / non évaluable),
     sha256 des octets bruts (ADR-0005 : hash toujours).
  3. **R1** — p̂ᵢ, n, K, P̂₀/P̂₁/P̂_more, z **ou** « historique insuffisant »,
     comptes « hors-env non évaluable » par source, et A(window-stationarity).

`render_report` ne lit QUE les fichiers de journal → recalculable par un tiers.
Sortie **déterministe** (mêmes fichiers → même texte) : c'est la répétition
générale du claim de recalculabilité (plan §5).
"""

from __future__ import annotations

import os
import sys
from decimal import Decimal

from . import records
from .r1 import (
    A_WINDOW_STATIONARITY,
    classify_cells,
    compute_r1,
    parse_journal,
)


def _fmt_dec(x) -> str:
    """Decimal → chaîne exacte (recalculable) ; None → tiret."""
    return "-" if x is None else str(x)


def render_report(control_path: str, journal_path: str) -> str:
    params_list, clock_checks, markers = records.parse_control(control_path)
    # Concordance des run_params successifs (fail-closed, §E) — même garde que
    # l'oracle : une table depuis des seuils divergents serait un mensonge.
    params = records.effective_run_params(params_list)
    readings = parse_journal(journal_path)
    pool = list(params["pool"])
    w = int(params["w"])
    sigma = Decimal(str(params["sigma_classe"]))
    tau = Decimal(str(params["tau_classe"]))
    seuil_hist = Decimal(str(params.get("seuil_historique_valeur", 10)))
    n_min = int(params.get("n_min_hors_enveloppe", 4))

    r1 = compute_r1(markers, readings, pool, w, sigma, tau, seuil_hist, n_min)
    cells = classify_cells(markers, readings, pool, w, sigma, tau, n_min)
    reading_map = {(int(r["window_start"]), r["flux_id"]): r for r in readings}

    out: list[str] = []
    ap = out.append

    # ── Bloc 1 : Paramètres ────────────────────────────────────────────────
    ap("=" * 78)
    ap("TABLE §6 (skeleton S2 Phase A) — recalculable depuis le journal seul (ADR-0003)")
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
            ap("    z       = HISTORIQUE INSUFFISANT (n·P̂_more·(1−P̂_more) < 10, 10 §5.4)"
               " — pas de z publié ; aucun z non significatif n'est présenté comme "
               "absence de dépendance (04 §2)")
        else:
            ap(f"    z       = {_fmt_dec(blk['z'])} (seuil {_fmt_dec(blk['seuil_z'])}, "
               f"unilatéral — 10 §5.1)")
    ap(f"\n  {A_WINDOW_STATIONARITY}")
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
