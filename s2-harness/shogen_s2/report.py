"""Table de sortie §6 — recalculable offline (ADR-0003). COMPLÈTE (6 blocs) à M1c.

Conception : docs/10-mesures-pilotes-design.md §6 (« tout chiffre du rapport se
recalcule depuis le journal par un lecteur sans accès à Shōgen », ADR-0003).

Six blocs (§6), tous calculés à M1c :
  1. **Paramètres** — depuis `run_params` : pool, w, seuils, précision, version,
     dates, calendrier de strates committé, contrôle d'horloge, **composition de
     devise du pool** (§2, devise marquée) + résidu de peg USDT/USD = R2(2a) ρ_resid,
     CALCULÉ au bloc 5 (référence croisée).
  2. **Journal brut** — par fenêtre×source : valeur, devise, horodatage porté,
     statut d'écart, sha256 des octets bruts (ADR-0005 : hash toujours).
  3. **R1** — p̂ᵢ, n, K par strate, P̂₀/P̂₁/P̂_more, z **ou** la **queue binomiale
     exacte** sous la garde (§5.4) **ou** « historique insuffisant » nu (dégénéré),
     comptes non évaluables, A(window-stationarity).
  4. **L&M** — Ê(Θ), Ê(Θ²), Var̂(Θ) par strate, corrélations φ **signées** par
     paire de flux ; matrice de co-écarts complète (consommée par le drapeau 2 §5.6,
     bloc 6) ; corrélations entre CLUSTERS et agrégation flux→source réalisées au
     bloc 5 (requièrent la partition R2).
  5. **R2** (r2.py) — table ASN datée (§4.1) ; les 5 statistiques de contenu par
     paire (ρ_raw, ρ_resid, T/T_Δ, (K,z), δ), jamais fusionnées (§4.2) ; arêtes
     méthode `basis:doc` avec doc_url/doc_fetched (§4.3) ; les 7 résidus §4.1.
  6. **Tête de certificat** — partition NOMMÉE, **k_eff, k nominal**, les DEUX
     drapeaux (« historique insuffisant » §5.4 ; « co-défaillance non expliquée par
     R2 » §5.6, tri-état).

`render_report` ne lit QUE les fichiers de journal → recalculable par un tiers.
Sortie **déterministe** (mêmes fichiers → même texte) : répétition générale du
claim de recalculabilité (plan §5).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from decimal import Decimal, localcontext

from . import r2, records
from .lm import compute_lm
from .r1 import (
    A_WINDOW_STATIONARITY,
    DECIMAL_PREC,
    ELL_BLOC,
    ETIQUETTE_POOLEE,
    GARDE_BLOCS,
    SEUIL_Z,
    analysis_pools,
    bornes_censure,
    build_window_strate,
    classify_cells,
    compute_r1,
    fenetres_sautees,
    parse_journal,
    regle_critere,
)
from .window import STRATE_DEFAUT, verify_markers_against_spec, weekday_utc

ETIQUETTE_Z_BLOC = ("plancher d'erreur-type pré-enregistré (blocs mobiles, noyau de Bartlett ; "
                    "ADR-0028 §1 bis) — z_s reste la statistique confirmatoire")   # ADR-0028 §1 bis.2
A_WINDOW_DEPENDENCE = (                    # registre 08, colonne « exercée par » ; lot B-DEP-2
    "A(window-dependence) engagée par le niveau de R1 (ADR-0028 §1 bis.1 pt 7 ; registre 08) : dépendance "
    f"sérielle de I_t = 1{{m_t ≥ 2}} d'une strate de portée < ℓ = {ELL_BLOC} fenêtres ; exercée par z_bloc "
    "et le diagnostic de runs de I_t ; décharge = SHOGEN-DEP-FENETRES-2 (08 ; ADR-0028 annexe B.6)")
# ADR-0028 annexe D.5 (SHOGEN-CENSURE-INFO-1 ; CV2-24, CV2-26) : étiquette imposée, C-7 du cp-1 de D5-AMEND
ETIQUETTE_CENSURE = ("bornes à P̂_more fixé, non extérieures ; verdict non identifié sous censure arbitraire "
                     "des fenêtres sautées")


def _fmt_dec(x) -> str:
    """Decimal → chaîne exacte (recalculable) ; zéro Decimal exact → « 0 », forme unique quel que soit l'exposant
    hérité du calcul (SHOGEN-RENDU-ZERO-1) ; None → tiret."""
    return "-" if x is None else "0" if isinstance(x, Decimal) and x == 0 else str(x)


def _iso_utc(ts) -> str:
    """epoch → ISO-8601 UTC (déterministe) pour la colonne « heure » de la table ASN
    (§6 bloc 5 : « résolveur, heure »). None → tiret."""
    if ts is None:
        return "-"
    from datetime import datetime, timezone
    return datetime.fromtimestamp(float(ts), timezone.utc).isoformat()


def _comptes(recs, strates) -> list:
    """(marqueurs, clock_checks, asn) → fenêtres DISTINCTES par strate (dédup de n), asn, horloges."""
    ws = build_window_strate(recs[0])
    return [sum(1 for s in ws.values() if s == st) for st in strates] + [len(recs[2]), len(recs[1])]


def _retires(avant, apres, strates) -> str:
    """Comptes retirés d'`avant` à `apres` (bloc 1 ; ADR-0028 D5, SHOGEN-EXCL-COMPTE-1) ; asn_attribution
    ventilées par valeur du statut de l'enregistrement, sur la même assiette (SHOGEN-ASN-STATUT-1)."""
    d = [x - y for x, y in zip(_comptes(avant, strates), _comptes(apres, strates))]
    fen = ", ".join(f"{st} {k}" for st, k in zip(strates, d)) or "0 (aucune fenêtre au journal)"
    st = Counter(r.get("status") for r in avant[2]) - Counter(r.get("status") for r in apres[2])
    ven = ", ".join(f"{'sans statut' if k is None else k} {v}" for k, v in sorted(st.items(), key=str))
    return (f"fenêtres distinctes (window_close) {fen} ; asn_attribution {d[-2]}" + (f" ({ven})" if ven else "")
            + f" ; clock_check {d[-1]}")


def _duree(s: int) -> str:
    """Durée exacte de `s` secondes (fenêtres × w) : « H h MM min », puis « SS s » si non nul."""
    return f"{s // 3600} h {s % 3600 // 60:02d} min" + (f" {s % 60:02d} s" if s % 60 else "")


def _week_ends(ws_strate: dict, spec: dict) -> dict:
    """{(début, fin) : fenêtres distinctes de la strate stress} ; week-end = suite maximale de jours UTC
    dont le jour (lundi = 0) est dans `stress_weekdays` (ADR-0025 déc. 4) ; ni vide ni plein (appelant)."""
    jours, j, out = set(spec["stress_weekdays"]), 86400, {}
    for ws, st in ws_strate.items():
        if st == spec["stress"]:
            a = b = ws // j
            while weekday_utc((a - 1) * j) in jours:
                a -= 1
            while weekday_utc((b + 1) * j) in jours:
                b += 1
            out[a * j, (b + 1) * j] = out.get((a * j, (b + 1) * j), 0) + 1
    return out


def _ligne_variante(st: str, nom: str, blk) -> str:
    """Une ligne de la table de sensibilité (R1 seul) ; `blk` None : strate absente de la variante."""
    tete = f"  {st:8} {nom:22} : "
    if blk is None:
        return tete + "absente (0 fenêtre retenue)"
    zs = f"z = {_fmt_dec(blk['z'])}" if blk["z"] is not None else (
        f"z non publié (garde §5.4 : n·P̂_more·(1−P̂_more) < {_fmt_dec(blk['seuil_historique'])}) ; " + (
            f"queue exacte P(K ≥ K_obs | Bin(n, P̂_more)) = {_fmt_dec(blk['queue_binomiale_P_K_ge_Kobs'])}"
            if blk["queue_exacte_applicable"] else "queue dégénérée (P̂_more ∈ {0,1})"))
    return (tete + f"n = {blk['n']} ; K = {blk['K']} ; P̂_more = {_fmt_dec(blk['P_more'])} ; {zs} ; "
            f"drapeau 1 = {blk['flag_historique_insuffisant']}")


def render_report(control_path: str, journal_path: str, exclude_ranges=(), segment=None) -> str:
    ranges = records.exclusion_ranges(exclude_ranges)   # ADR-0025 ; défaut : aucune
    params_list, clock_checks, markers = records.parse_control(control_path)
    asn_records = records.parse_asn(control_path)
    # Concordance des run_params successifs (fail-closed, §E) — même garde que
    # l'oracle. La table M1c calcule les 6 blocs → clés R1 **ET** R2 exigées présentes
    # (un run_params amputé d'une clé de partition n'est pas recalculable, §E).
    params = records.effective_run_params(
        params_list,
        load_bearing=records.LOAD_BEARING_KEYS + records.R2_LOAD_BEARING_KEYS,
    )
    # Strates journalées == calendrier committé (fail-closed, §5.3) — même garde
    # que l'oracle : une table sur des strates trafiquées serait un mensonge. Clés
    # porteuses PRÉSENTES (garanties par effective_run_params), lues sans défaut.
    div = verify_markers_against_spec(markers, params["strate_calendar"])
    if div:
        raise ValueError(
            f"strates journalées incohérentes avec le calendrier committé (§5.3) : {div[:5]}"
        )
    # Filtre de lecture unique APRÈS la garde §5.3 (ADR-0028 D5) : blocs 1-6 sur les enregistrements retenus.
    tous = (markers, clock_checks, asn_records)      # assiette des comptes et dates du bloc 1 (avant filtre)
    markers, clock_checks, asn_records, seg = records.filtre_lecture(params, *tous, ranges, segment)
    readings = parse_journal(journal_path)
    pool = list(params["pool"])
    w = int(params["w"])
    # σ PAR CLASSE + τ RELATIF (ADR-0021) — même décodage partagé que les 3 autres
    # lecteurs recalculables (records.sigma_tau_from_params), zéro divergence.
    sigma_by_class, sigma_class_of_flux, tau = records.sigma_tau_from_params(params)
    seuil_hist = Decimal(str(params["seuil_historique_valeur"]))
    n_min = int(params["n_min_hors_enveloppe"])
    # Pool d'analyse (ADR-0028 D1) APRÈS l'exclusion : blocs 3-6 ; bloc 2 (journal brut) : pool.
    pools, pool_an, retraits = analysis_pools(markers, readings, pool)
    cas_b = any(ps != pool_an for ps in pools.values())

    r1 = compute_r1(markers, readings, pool_an, w, sigma_by_class, sigma_class_of_flux,
                    tau, seuil_hist, n_min, pools)
    rg = regle_critere(r1)                 # règle SHOGEN-CRITERE-R1-1 (ADR-0028 §1 bis.1) : bloc 3
    cells = classify_cells(markers, readings, pool, w, sigma_by_class,
                           sigma_class_of_flux, tau, n_min)
    reading_map = {(int(r["window_start"]), r["flux_id"]): r for r in readings}
    # R2 complet (partition/k_eff, contenu, méthode, clusters, drapeau 2) — recalculé
    # depuis les mêmes enregistrements (ADR-0003). Le peg (bloc 1) le référence.
    r2_out = r2.compute_r2(markers, readings, asn_records, pool_an, w, sigma_by_class,
                           sigma_class_of_flux, tau, params, n_min_horsenv=n_min,
                           pool_by_strate=pools)

    out: list[str] = []
    ap = out.append

    # ── Bloc 1 : Paramètres ────────────────────────────────────────────────
    ap("=" * 78)
    ap("TABLE §6 (S2 Phase A — M1c, COMPLÈTE 6 blocs) — recalculable depuis le "
       "journal seul (ADR-0003)")
    ap("=" * 78)
    ap("\n[BLOC 1] PARAMÈTRES")
    cles = ("harness_version", "classe", "pool", "w", "sample_lead",
            "sigma_classe", "sigma_class_of_flux", "tau_classe", "kappa",
            "seuil_historique_valeur",
            "n_min_hors_enveloppe", "strate_defaut", "decimal_prec",
            "seuil_historique", "seuil_z", "residu_staleness",
            "n_windows_demande", "started_utc", "note_skeleton")
    for key in cles:
        if key in params:
            ap(f"  {key:24} = {params[key]}")
    ap(f"  {'run_params_demarrages':24} = {len(params_list)} (concordants sur les "
       f"champs porteurs — §E)")
    if "strate_calendar" in params:
        sc = params["strate_calendar"]
        ap(f"  {'strate_calendar':24} = kind={sc.get('kind')} "
           f"{sc.get('note', '')}".rstrip())
    ws_tous = build_window_strate(tous[0])          # HS2-05 : journal entier, avant segment et exclusion
    strates, deb = sorted(set(ws_tous.values())), sorted(ws_tous)
    ap(f"  {'campagne_fenetres':24} = {len(deb)} fenêtres distinctes au journal (window_close, avant "
       "segment et exclusion)" + (f" : première {deb[0]} = {_iso_utc(deb[0])} ; dernière {deb[-1]} = "
                                  f"{_iso_utc(deb[-1])} (window_start)" if deb else "") + " — HS2-05")
    ap(f"  {'portee_run_params':24} = journal entier, jamais segmenté ni exclu (§E) : run_params_demarrages"
       " = tous les démarrages ; started_utc, n_windows_demande = dernier démarrage (HS2-05)")
    nb = [k for k in cles if k in params and k not in records.LOAD_BEARING_KEYS + records.R2_LOAD_BEARING_KEYS]
    ap(f"  {'run_params_non_porteurs':24} = valeurs distinctes sur les {len(params_list)} démarrages, par clé non "
       "porteuse imprimée ci-dessus (valeur du dernier démarrage, hors contrôle de concordance §E) : " + ", ".join(
           f"{k} {len({json.dumps(p.get(k), sort_keys=True) for p in params_list})}" for k in nb)
       + " — SHOGEN-BLOC1-RUNPARAMS-1")
    dans_seg = records.filtre_lecture(params, *tous, (), segment)[:3]   # assiette des comptes par plage
    if seg is not None:
        ap(f"  {'segment':24} = [{seg[0]} ; {seg[1]}) = [{_iso_utc(seg[0])} ; {_iso_utc(seg[1])}) "
           "semi-ouvert, fin exclue, même borne sur window_start, ts, harness_ts (run_params conservés) ; "
           f"n fixe = {_fmt_dec(segment.get('n_fixe'))} — ADR-0028 D4, D2 pt 6")
        ap(f"  {'segment_retraits':24} = hors segment : {_retires(tous, dans_seg, strates)} — ADR-0028 D4")
    else:
        ap(f"  {'segment':24} = aucun (journal entier) — ADR-0028 D4")
    pertes = []                # → [SENSIBILITÉ] (annexe D.5, SHOGEN-DP-JOURNAL-LOSS-1), sans second calcul
    for a, b in ranges:        # uniquement si filtre (sans option : aucune ligne ajoutée)
        ap(f"  {'exclusion_window_start':24} = [{a} ; {b}] = [{_iso_utc(a)} ; "
           f"{_iso_utc(b)}] fermée, bornes incluses : hors n, K, P̂_more de toutes les "
           "strates (filtre du lecteur, journal intact) — harnais dégradé, ADR-0025")
        ap(f"  {'exclusion_ts_harness_ts':24} = [{a} ; {b + w}) = [{_iso_utc(a)} ; {_iso_utc(b + w)}) "
           "semi-ouvert : asn_attribution (ts), clock_check (harness_ts), "
           f"w = {w} s de run_params — ADR-0028 D5")
        seule = records.filtre_lecture(params, *dans_seg, [(a, b)])[:3]
        r = _retires(dans_seg, seule, strates)
        pertes.append(f"[{a} ; {b}] seule : {r}")
        ap(f"  {'exclusion_retraits':24} = [{a} ; {b}] seule (assiette : ligne segment) : {r}")
    if ranges:                 # C-4 (i) : chaque plage seule, puis l'union (chevauchement compté une fois)
        r = _retires(dans_seg, (markers, clock_checks, asn_records), strates)
        pertes.append(f"union de {len(ranges)} plage(s) : {r}")
        ap(f"  {'exclusion_retraits_union':24} = {len(ranges)} plage(s), union (assiette : ligne segment) : "
           f"{r} — SHOGEN-EXCL-COMPTE-1")
    sautees = fenetres_sautees(ws_tous, params["strate_calendar"], w, seg, ranges)   # ADR-0028 annexe D.5
    bs, ss = seg or (deb and (deb[0], deb[-1] + w)), ", ".join(
        f"{st} {sautees.get(st, 0)}" for st in sorted({*strates, *sautees}))
    port = "segment" if seg else "journal entier : première fenêtre ; dernière + w"
    ap(f"  {'fenetres_sautees':24} = " + (f"grille de pas w = {w} s sur [{bs[0]} ; {bs[1]}) ({port}), sans "
       f"marqueur window_close, hors plages D5 : {ss}" if bs else "aucune fenêtre au journal") + " — toutes "
       "causes confondues, sous l'hypothèse H_perte (pertes d'outillage non informatives : "
       "A(loss-non-informative), registre 08) ; ADR-0028 annexe D.5, SHOGEN-CENSURE-INFO-1")
    for st, f, k_ok, k_tot, n_s in retraits:   # ADR-0028 D1 (c) : uniquement si retrait
        cas = "(a), hors R2 aussi" if f not in pool_an else "(b), gardé par R2"
        ap(f"  {'pool_analyse_retrait':24} = {f} strate « {st} » : ok = {k_ok} / {k_tot} "
           f"lectures, n = {n_s} — hors R1 et L&M de la strate, cas {cas} (ADR-0028 D1)")
    for st, ps in (pools.items() if retraits else ()):
        ap(f"  {'k_nominal_strate':24} = « {st} » : "
           f"{len(r2.hosts_of_pool(params['flux_hosts'], ps))} sources / {len(ps)} "
           "flux (pool d'analyse, ADR-0028 D1)")
    # Devise MARQUÉE par flux (§2, décision 4) : composition du pool + résidu peg
    # (le démêlage USDT/USD est R2(2a) ρ_resid, CALCULÉ au bloc 5 — référencé ici).
    cur_by_flux: dict = {}
    for r in readings:
        c = r.get("currency")
        if c is not None and r["flux_id"] in pool_an:   # pool d'analyse (ADR-0028 D1)
            cur_by_flux.setdefault(r["flux_id"], c)
    n_usd = sum(1 for c in cur_by_flux.values() if c == "USD")
    n_usdt = sum(1 for c in cur_by_flux.values() if c == "USDT")
    ap(f"  {'devise_composition':24} = {n_usd} USD / {n_usdt} USDT (classe "
       f"« BTC/USD-stable », devise marquée par flux — 10 §2/§9.4)")
    peg_keys = [k for k, v in r2_out["content"]["pairs"].items() if v["is_peg_usdt_usd"]]
    ap(f"  {'residu_peg_usdt_usd':24} = écart de peg USDT/USD = résidu R2(2a) ρ_resid — "
       f"CALCULÉ au bloc 5 (paires USDT×USD : {len(peg_keys)}) (10 §2/§9.4)")
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
    ap("  définition d'écart (10 §5.2 ; τ relatif : ADR-0020 déc. 2, ADR-0022 ; r1.classify_ecart), par fenêtre "
       "et par flux du pool d'analyse, "
       "précédence panne > staleness > hors-enveloppe : panne = lecture absente, statut ≠ ok ou prix "
       "absent ; staleness = win_end − source_ts > σ_classe de la classe du flux (σ_classe ou source_ts "
       "absent : non évaluée) ; hors-enveloppe = |p − médiane_LOO|/médiane_LOO > τ_classe, N ≥ n_min "
       "répondantes ; N < n_min, médiane_LOO ≤ 0 ou τ_classe absent : non évaluable (pas un écart) ; sinon "
       "pas d'écart ; K = fenêtres à ≥ 2 écarts — HS2-06")
    ap(f"  paramètres (run_params, bloc 1) : σ_classe = {params['sigma_classe']} ; τ_classe = "
       f"{params['tau_classe']} ; n_min = {n_min}")
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
        for f in blk["per_source"]:            # pool d'analyse de la strate (ADR-0028 D1)
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
            ap("    z       = non publié (garde §5.4 : n·P̂_more·(1−P̂_more) < "
               f"{_fmt_dec(blk['seuil_historique'])}) — "
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
    if r1.get("strates"):     # ADR-0028 §1 bis.1 pts 3 et 9 (A-2) : clé « bloc » de r1, sans recalcul
        ap(f"\n  ── z_bloc par strate : {ETIQUETTE_Z_BLOC}")
        ap("    z_bloc = (K − n·P̂_more)/σ̂_bloc, même numérateur que z ; σ̂²_bloc = γ̂₀ + 2·Σ_{k=1}^{ℓ−1} "
           "(1 − k/ℓ)·γ̂_k sur la série I_t = 1{m_t ≥ 2} de la strate, γ̂_k centrés sur Ī = K/n, lag sur la "
           "grille de pas w : paires de deux fenêtres de la strate, fenêtre absente sans paire")
        ap(f"    z_bloc publié si σ̂²_bloc > 0 et n ≥ {GARDE_BLOCS}·ℓ (garde de blocs, distincte du "
           "drapeau 1), que la garde §5.4 soit tenue ou non ; FIV = σ̂²_bloc/(n·P̂_more·(1 − P̂_more)) = "
           "R_centrage × FIV_série, R_centrage = γ̂₀/(n·P̂_more·(1 − P̂_more)), FIV_série = σ̂²_bloc/γ̂₀ ; "
           "cv théorique = √(4ℓ/(3n)) [inféré : dérivation de l'AVIS-advisor-defi Q1 (iv)]")
        for st, blk in r1["strates"].items():
            b, ru = blk["bloc"], blk["bloc"]["runs"]
            ap(f"    « {st} » : ℓ = {b['ell']} ; γ̂₀ = {_fmt_dec(b['gamma0'])} ; σ̂²_bloc = "
               f"{_fmt_dec(b['sigma2_bloc'])} ; cv théorique = {_fmt_dec(b['cv_theorique'])} [inféré]")
            ap(f"    « {st} » : " + (b["FIV_motif"] or f"FIV = {_fmt_dec(b['FIV'])} ; R_centrage = "
                                    f"{_fmt_dec(b['R_centrage'])}")
               + " ; " + (b["FIV_serie_motif"] or f"FIV_série = {_fmt_dec(b['FIV_serie'])}"))
            ap(f"    « {st} » : z_bloc = " + (f"non publié : {b['z_bloc_motif']}" if b["z_bloc"] is None
                                             else _fmt_dec(b["z_bloc"])))
            ap(f"    « {st} » : diagnostic de runs de I_t (hors décision) : nombre = {ru['nombre']} ; "
               f"longueur moyenne = {_fmt_dec(ru['longueur_moyenne'])} ; run maximal = {ru['run_max']}")
    sc = params["strate_calendar"]      # famille D2 pt 4 ; m dynamique (§1 bis.1 pt 6), prémisse (pt 7)
    ap("\n  famille de Bonferroni pré-enregistrée (ADR-0028 D2 pt 4) : " + (
        f"m = {rg['m']} (strates testées : {', '.join(rg['testees']) or 'aucune'} ; m ≤ 2 ; "
        "§1 bis.1 pt 6), tests unilatéraux au seuil 2,33 ; borne P(au moins un rejet à tort) ≤ "
        "2 × 0,01 = 0,02 sous le modèle nul joint (§1 bis.1 pt 7) : modèle d'indépendance du pool de "
        "doc 10 §5.1 et dépendance sérielle des fenêtres de portée < ℓ = "
        f"{ELL_BLOC} (A(window-dependence), registre 08) ; niveau asymptotique, non démontré ≤ 0,01 en "
        "échantillon fini (SHOGEN-SIM-NIVEAU-1)" if sc.get("kind") == "weekend_utc"
        else "non applicable (calendrier mono-strate)"))
    po = r1["poolee"]                   # hors de r1["strates"] : ni règle, ni drapeau 2, ni famille
    ap(f"\n  ── strate poolée (ADR-0028 D2 pt 4 ; {ETIQUETTE_POOLEE}) : forme stratifiée, jamais l'union "
       "brute des fenêtres")
    ap("    z_pool = Σ_s (K_s − n_s·P̂_more,s) / √(Σ_s n_s·P̂_more,s·(1 − P̂_more,s)), chaque strate sur son "
       "pool d'analyse D1")
    for st, e in po["strates"].items():
        ap(f"    « {st} » : n = {e['n']} ; K = {e['K']} ; P̂_more = {_fmt_dec(e['P_more'])} ; pool d'analyse "
           f"D1 = {e['N']} flux")
    if po["z_pool"] is None:
        ap(f"    z_pool  = non publié : {po['motif']}")
    else:
        ap(f"    Σ_s (K_s − n_s·P̂_more,s) = {_fmt_dec(po['numerateur'])} ; "
           f"Σ_s n_s·P̂_more,s·(1 − P̂_more,s) = {_fmt_dec(po['variance'])}")
        ap(f"    z_pool  = {_fmt_dec(po['z_pool'])} — {ETIQUETTE_POOLEE}")
    ap(f"\n  {A_WINDOW_STATIONARITY}")
    ap(f"  {A_WINDOW_DEPENDENCE}")
    # Règle SHOGEN-CRITERE-R1-1 (ADR-0028 §1 bis.1 pts 5, 6, 8) : valeurs de r1.regle_critere, sans recalcul
    ap("\n  ── règle SHOGEN-CRITERE-R1-1 (ADR-0028 §1 bis.1 pts 1-11 ; forme scellée) : valeur par strate ; "
       "comparaisons sur les Decimal publiées, non arrondies, au seuil 2.33, « ≥ » ; aucune p-valeur")
    kp = r2_out["partition"]
    ke = ("= non évaluable" if kp["k_eff"] is None else f"≤ {kp['k_eff']} (borne supérieure)"
          if kp.get("k_eff_is_upper_bound") else f"= {kp['k_eff']}")
    suites = {"garde_5_4": " : strate non testée, hors décision (§1 bis.1 pt 2)",
              "rejet_non_qualifiable": " : rejet non qualifiable : niveau non tenu sous dépendance sérielle",
              "discordance": " (discordance)"}
    for st, e in rg["strates"].items():
        blk, cas, tete = r1["strates"][st], e["cas"], f"    « {st} » : "
        z, zb, src = blk["z"], blk["bloc"]["z_bloc"], blk["per_source"].values()
        fo, ne = blk["residu_staleness_fail_open"], sum(s["non_eval_hors_env"] for s in src)   # AXES-ENONCE-1 (b)
        res = [f"staleness fail-open : {', '.join(fo)}"] * bool(fo) + [
            f"hors-enveloppe non évaluable : {ne} cellules (fenêtre, flux)"] * bool(ne)
        axes = "axes " + " / ".join(a.replace("_", "-") for a in ("panne", "staleness", "hors_enveloppe") if any(
            a in s["axes_evaluables"] for s in src)) + f" (résidu : {' ; '.join(res) or 'aucun'})"
        zs = (f"z_s non publié (garde §5.4 : n·P̂_more·(1 − P̂_more) < {_fmt_dec(blk['seuil_historique'])})"
              if z is None else
              f"z_s = {_fmt_dec(z)} {'<' if cas == 'z_sous_seuil' else '≥'} 2,33"
              + (" (z_s ≤ −2,33 : hors famille, sans conclusion)" if z <= -SEUIL_Z else ""))
        zbt = ("" if cas in ("garde_5_4", "z_sous_seuil") else
               f" ; z_bloc non publié ({blk['bloc']['z_bloc_motif']})" if zb is None else
               f" ; z_bloc = {_fmt_dec(zb)} {'≥' if cas == 'rejette' else '<'} 2,33")
        ap(f"{tete}{zs}{zbt} → {e['valeur']}{suites.get(cas, '')}")
        if cas == "rejette":
            ap(f"{tete}« le modèle d'indépendance du pool (k nominal_s = {len(blk['per_source'])} flux "
               f"du pool de la strate, bloc 1 ; k_eff mesuré {ke}, bloc 6) est rejeté dans la strate {st} "
               f"sur {blk['n']} fenêtres, {axes}, tel qu'observé par cet instrument (hôte, DNS et réseau du "
               "harnais compris) ; aucune dépendance de paire n'est établie »")
        elif cas == "discordance":
            ap(f"{tete}« le modèle binomial de doc 10 §5.1, à fenêtres indépendantes, est rejeté ; la cause "
               "n'est pas identifiée entre co-défaillance des sources et dépendance sérielle des fenêtres »")
        elif cas == "z_sous_seuil":
            ap(f"{tete}« le modèle d'indépendance n'est pas rejeté sur {blk['n']} fenêtres, {axes} » ; un "
               "résultat négatif est un résultat")
        if e["emd"] is not None:
            ap(f"{tete}EMD_s = (2,33 + 0,8416)·max(√(n_s·P̂_more,s·(1 − P̂_more,s)), σ̂_bloc,s) = "
               f"{_fmt_dec(e['emd'])} fenêtres ; fraction de n_s = {_fmt_dec(e['emd_fraction'])} "
               "(puissance 0,8 : choix de conception ; aucun seuil sur l'EMD)")
        ru, lb = blk["bloc"]["runs"]["run_max"], blk["bloc"]["ell"]
        if ru >= lb:                     # ADR-0028 §1 bis.1 pt 9 : hors décision, sans effet sur la valeur
            ap(f"{tete}drapeau « run maximal ≥ ℓ » (run maximal = {ru} ≥ ℓ = {lb}) : σ̂²_bloc,s biaisé vers "
               "le bas ; SHOGEN-DEP-FENETRES-2 prioritaire avant G10 — hors décision, sans effet sur la "
               "valeur")
    nq, tst = rg["non_qualifiables"], rg["testees"]
    ap(f"  « R1 discrimine » (§1 bis.1 pt 6 ; déclencheur de D6 (vi) et D9) = {rg['r1_discrimine']} : "
       + (f"strate(s) qui rejettent : {', '.join(rg['rejette'])}" if rg["rejette"] else
          "aucune strate ne rejette ; " + (f"rejet non qualifiable : {', '.join(nq)}" if nq else
                                           f"strate(s) testée(s) : {', '.join(tst)}" if tst
                                           else "aucune strate testée")))
    # Traitements de l'annexe D.5 d'ADR-0028 (amendement du 2026-09-30, A-6) : valeurs de r1, sans recalcul
    ap("\n  ── traitements pré-enregistrés de l'annexe D.5 d'ADR-0028 (amendement du 2026-09-30, A-6) : "
       "descriptifs, hors décision, sans paramètre")
    ap("    τ observé (SHOGEN-TAU-REDERIV-1), sans ré-estimation de τ : |p − médiane_LOO|/médiane_LOO des "
       "cellules (fenêtre, flux) arrivées à l'axe (i) (hors-enveloppe ou pas d'écart), pool d'analyse D1 de "
       "chaque strate, sur le segment, par classe (sigma_class_of_flux) ; P99 au rang le plus proche, rang "
       "(99·N + 99)//100")
    for cl, t in r1["tau_observe"].items():
        ap(f"    « {cl} » : τ_classe = {_fmt_dec(t['tau_classe'])} ; N = {t['N']}" + (
            f" ; P99 = {_fmt_dec(t['P99'])} ; maximum = {_fmt_dec(t['max'])}" if t["N"] else " : non défini"))
    ap("    décomposition de K (SHOGEN-HOST-DEGRADED-1) par nombre de lectures présentes au statut "
       "panne_transport (model.Status) des flux du pool D1 de la strate ; c_s = fenêtres où chaque flux du "
       "pool porte une lecture panne_transport ; le z confirmatoire inclut les modes communs de "
       "l'observateur (hôte, DNS, réseau)")
    for st, blk in r1.get("strates", {}).items():
        d = blk["decomposition_K"]
        ap(f"    « {st} » : K = {blk['K']} = K[≥ 2 panne_transport] {d['pt_2_plus']} + K[1] {d['pt_1']} + "
           f"K[0] {d['pt_0']} ; K[tous les écarts hors_enveloppe] = {d['tous_hors_enveloppe']} ; c_s = "
           f"{d['c']}")
    ap(f"    fenêtres sautées (SHOGEN-CENSURE-INFO-1 ; s au bloc 1) : {ETIQUETTE_CENSURE}")
    ap("    z_bas = (K − (n + s)·P̂_more)/√((n + s)·P̂_more·(1 − P̂_more)) ; z_haut = (K + s − (n + s)·"
       "P̂_more)/√((n + s)·P̂_more·(1 − P̂_more)) ; puis σ̂_bloc au dénominateur si z_bloc est publié ; "
       "hypothèse H_perte")
    for st, blk in r1.get("strates", {}).items():
        s, zb = sautees.get(st, 0), blk["bloc"]["z_bloc"] is not None
        if blk["z"] is None:
            ap(f"    « {st} » : s = {s} ; bornes non publiées (garde §5.4 : z_s non publié)")
            continue
        b = bornes_censure(blk["n"], blk["K"], blk["P_more"], s, blk["bloc"]["sigma2_bloc"] if zb else None)
        ap(f"    « {st} » : s = {s} ; z_bas = {_fmt_dec(b['z_bas'])} ; z_haut = {_fmt_dec(b['z_haut'])} ; "
           "avec σ̂_bloc : " + (f"z_bas = {_fmt_dec(b['z_bloc_bas'])} ; z_haut = "
                               f"{_fmt_dec(b['z_bloc_haut'])}" if zb else "non publiées (z_bloc non publié)"))

    # ── Bloc 4 : L&M (§5.5) ────────────────────────────────────────────────
    lm_out = compute_lm(markers, readings, pool_an, w, sigma_by_class,
                        sigma_class_of_flux, tau, n_min, pools)
    ap(f"\n[BLOC 4] L&M (§5.5) — fonction de difficulté Θ ; N = {lm_out['N']} flux "
       + ("(pool d'analyse ; N par strate ci-dessous, ADR-0028 D1)" if cas_b else "(pool)"))
    for st, blk in lm_out["strates"].items():
        ap(f"\n  ── strate « {st} » : n = {blk['n']} ; Σ mⱼ = {blk['sum_m']}"
           + (f" ; N = {blk['N']}" if cas_b else ""))
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
        # le co-écart le plus extrême) et φ=0. CONSOMMÉE par le DRAPEAU 2 (§5.6) au
        # bloc 6 (localisation inter-clusters) ; la donnée (n11..n00) est livrée ici.
        ap("    matrice de co-écarts COMPLÈTE (§6 bloc 4 ; consommée par le drapeau 2 "
           "§5.6 au bloc 6) — par paire [n11 n10 n01 n00] φ (co-écarts en tête) :")
        for k, v in sorted(pair_items, key=lambda kv: (-kv[1]["n11"], kv[0])):
            phi_s = _fmt_dec(v["phi"]) if v["phi"] is not None else "non_définie"
            ap(f"      {k:26} [{v['n11']} {v['n10']} {v['n01']} {v['n00']}] "
               f"φ={phi_s} ({v['signe']})")
        ap(f"    réalisé M1c (bloc 5) : {blk['renvoi_m1c_clusters']}")
        ap(f"    réalisé M1c (bloc 5) : {blk['renvoi_m1c_flux_source']}")
        ap(f"    caveat : {blk['caveat_non_eval']}")

    # ── Bloc 5 : R2 (ASN / contenu / méthode) — §4.1/§4.2/§4.3 ─────────────
    part = r2_out["partition"]
    ap("\n[BLOC 5] R2 — observables de diversité (10 §4)")

    # 5a. Table ASN datée (§4.1) — par hôte : IP, préfixe, ASN (2 bases), résolveur, heure
    ap("\n  (a) AXE ASN (§4.1) — attribution croisée ≥ 2 bases BGP (RIPEstat, Team Cymru)")
    if not part["asn_measured"] and not tous[2]:
        ap("      axe ASN NON MESURÉ : aucun enregistrement asn_attribution au journal "
           "(collect_asn non lancé — c'est l'orchestrateur qui le lance à la campagne).")
    elif not part["asn_measured"]:     # des sondes au journal, aucune retenue pour le pool (G2 B-SEG-1, (c))
        ap(f"      axe ASN NON MESURÉ : aucun enregistrement asn_attribution retenu pour les hôtes du pool — "
           f"{len(tous[2])} au journal, {len(asn_records)} retenus par le filtre de lecture (bloc 1).")
    ahdr = (f"      {'hôte':30} {'flux':18} {'résolveur':18} {'heure(UTC)':26} "
            f"{'IP':16} {'préfixe':16} {'RIPEstat':9} {'Cymru':7} {'holder':14} {'état'}")
    ap(ahdr)
    ap("      " + "-" * (len(ahdr) - 6))
    for h in part["hosts"]:
        rec = part["attribution_by_host"].get(h, {})
        st = part["asn_states"][h]
        flux = ",".join(part["flux_by_host"].get(h, []))
        ap(f"      {h:30} {flux:18} {str(rec.get('resolver') or '-'):18} "
           f"{_iso_utc(rec.get('ts')):26} {str(rec.get('ip') or '-'):16} "
           f"{str(rec.get('prefix') or '-'):16} {str(rec.get('asn_ripestat') or '-'):9} "
           f"{str(rec.get('asn_cymru') or '-'):7} {str(rec.get('holder') or '-'):14} "
           f"{st['kind']}")
        chain = rec.get("cname_chain") or []
        if chain:
            # chaîne CNAME datée (résidu 7) — le narratif ex. Binance → CloudFront (§4.1)
            ap(f"          CNAME: {h} → {' → '.join(chain)}")
    for dv in part["asn_divergences"]:
        ap(f"      DIVERGENCE ASN (résidu 4, instantanéité) hôte {dv['host']} : "
           f"{dv['avant']} → {dv['apres']} (publiée, jamais écrasée)")
    if part["merge_reasons"]:
        ap("      recouvrements MEASURED (fusionnent — jamais basis:doc seul, ADR-0008) :")
        for m in part["merge_reasons"]:
            if m["axis"] == "asn_measured":
                ap(f"        ASN partagé cross-confirmé AS{m['asn']} {m.get('holder') or ''} : "
                   f"{m['hosts']}")
            else:
                ap(f"        identité-copie contenu : flux {m['flux_pair']} → hôtes {m['hosts']}")
    else:
        ap("      aucun recouvrement measured (partition = singletons sur cet axe)")

    # 5b. Axe contenu (§4.2) — 5 statistiques PAR PAIRE, jamais fusionnées
    content = r2_out["content"]
    ap(f"\n  (b) AXE CONTENU (§4.2) — {content['n_windows']} fenêtres ; N_min = {content['n_min']} fenêtres "
       "communes par paire (choix de conception, doc 10 §4.2 b ; SE(artanh r) = 1/√(N−3), transformation de "
       "Fisher, Penn State STAT 509 L7 §7.8)")
    ap(f"      {content['grid_note']}")
    ap(f"      critère de fusion contenu v0 : {content['merge_criterion']}")
    ap(f"      {content['coab_staleness_note']}")
    ap("      par paire [ρ_raw ρ_resid | T T_Δ | co-aberrance K,z | δ lag] — jamais fusionnées :")
    for key in sorted(content["pairs"]):
        pr = content["pairs"][key]
        raw, res, tk, co, dl = (pr["rho_raw"], pr["rho_resid"], pr["tick"],
                                pr["coaberrance"], pr["delta"])
        tags = []
        if pr["basis_doc_triggered"]:
            tags.append("basis:doc→(b)")
        if pr["is_peg_usdt_usd"]:
            tags.append("peg USDT/USD=ρ_resid")
        if tk["exact_copy_merge"]:
            tags.append("COPIE-EXACTE→fusion")
        tagstr = (" {" + ", ".join(tags) + "}") if tags else ""
        if not raw["sufficient"] and not res["sufficient"]:
            ap(f"      {key:26} historique de contenu insuffisant "
               f"(ρ_raw n={raw['n']}, ρ_resid n={res['n']} < N_min){tagstr}")
        else:
            zc = (_fmt_dec(co['z']) if co.get('z') is not None
                  else (f"queue={_fmt_dec(co['queue'])}" if co.get('queue') is not None
                        else "insuff"))
            ap(f"      {key:26} ρ_raw={_fmt_dec(raw['rho'])} ρ_resid={_fmt_dec(res['rho'])} | "
               f"T={_fmt_dec(tk['T'])} T_Δ={_fmt_dec(tk['T_delta'])} | K={co['K']} z/{zc} | "
               f"δlag={dl['best_lag']}{tagstr}")

    # 5c. Axe méthode (§4.3) — 5 arêtes basis:doc, déclenchent (b), ne fusionnent pas
    ap("\n  (c) AXE MÉTHODE (§4.3) — arêtes `basis:doc` (ADR-0008 : déclenchent (b), "
       "ne partitionnent pas)")
    for e in r2_out["method_edges"]:
        if e["kind"] == "upstream":
            ap(f"      {e['from']} → {e['to']} [basis:{e['basis']}] {e['relation']}")
        else:
            ap(f"      {e['node']} estimateur [basis:{e['basis']}] : {e['estimator']}")
        ap(f"          doc_url={e['doc_url']} doc_fetched={e['doc_fetched']}")

    # 5d. Corrélations entre CLUSTERS (§5.5 pt 4) — réalisées ici (partition requise)
    cc = r2_out["cluster_correlations"]
    ap(f"\n  (d) CORRÉLATIONS ENTRE CLUSTERS (§5.5 pt 4) — {cc['convention']}")
    if cc["cluster_pairs"]:
        for k, v in sorted(cc["cluster_pairs"].items()):
            ap(f"      {k} : ρ(Θ̂)={_fmt_dec(v['rho'])} ({v['signe']}) [{v['note']}]")
    else:
        ap(f"      aucun cluster à ≥ 2 flux ({cc['n_multi_clusters']}) → tout reste au φ "
           "par paire de flux (bloc 4)")

    # 5e. Les 7 résidus de l'axe ASN (§4.1) — publiés avec l'observable
    ap("\n  (e) LES 7 RÉSIDUS DE L'AXE ASN (§4.1) — un observable est un témoignage "
       "avec ses résidus (04 §4) :")
    for r in r2_out["residus_asn"]:
        ap(f"      {r}")

    # ── Bloc 6 : Tête de certificat — k_eff, k nominal, les 2 drapeaux ─────
    ap("\n[BLOC 6] TÊTE DE CERTIFICAT (10 §5.6 / 04 §3)")
    ap(f"  k nominal = {part['k_nominal']} (hôtes distincts du pool)")
    if part.get("k_eff_is_upper_bound"):
        # BORNE SUPÉRIEURE (C-A) : ≥1 hôte non attribué gonfle k_eff — jamais lu comme
        # un compte d'indépendance CONFIRMÉ (04 §4.1).
        ap(f"  k_eff     ≤ {_fmt_dec(part['k_eff'])}  (BORNE SUPÉRIEURE ; "
           f"{part['n_unattributed']} hôte(s) non attribué(s) : {part['unattributed']}) "
           f"— {part['k_eff_note']}")
    else:
        ap(f"  k_eff     = {_fmt_dec(part['k_eff'])}  — {part['k_eff_note']}")
    hs = [h for h in part["hosts"] if h in part["attribution_by_host"]]      # hôtes du pool, relevé retenu
    ts = sorted(part["attribution_by_host"][h]["ts"] for h in hs)
    ap("  date de la partition, axe ASN (ADR-0026 déc. 1 ; HS2-07) = " + (
        f"relevé asn_attribution retenu (dernier par hôte, après filtre de lecture) : min {ts[0]} = "
        f"{_iso_utc(ts[0])} ; max {ts[-1]} = {_iso_utc(ts[-1])} ; {len(hs)} / {len(part['hosts'])} hôtes "
        "du pool" if ts else "non mesurée (aucun hôte du pool n'a de relevé asn_attribution retenu)")
       + " — descriptif seulement (ADR-0028 annexe D.5)")
    ap("  R3 (déclaration : entité légale, juridiction, méthodologie annoncée) ne "
       "modifie JAMAIS k_eff (§5.6 / 04 §3) — seuls les recouvrements R2 measured partitionnent.")
    ap("  PARTITION NOMMÉE (ADR-0007 : nomme l'amont, jamais un compte anonyme) :")
    for c in part["clusters"]:
        ap(f"    cluster = {c['name']} ; flux = {c['flux']}")
        for up in c["declared_upstreams"]:
            ap(f"        amont déclaré (basis:doc, ne fusionne pas) : {up['from']} → "
               f"{up['to']} ({up['doc_url']})")
        for cav in c["caveats"]:
            ap(f"        caveat : {cav}")
    # Drapeau 1 : historique insuffisant (§5.4), par strate (déjà au bloc 3)
    flags1 = {st: blk["flag_historique_insuffisant"]
              for st, blk in r1.get("strates", {}).items()}
    if r1.get("note"):
        flags1["(global)"] = r1["flag_historique_insuffisant"]
    ap(f"  DRAPEAU 1 « historique insuffisant » (§5.4) par strate : {flags1}")
    # Drapeau 2 : co-défaillance non expliquée par R2 (§5.6), tri-état
    d2 = r2_out["drapeau_2"]
    ap(f"  DRAPEAU 2 « co-défaillance observée non expliquée par les axes R2 » (§5.6) : "
       f"état = {d2['etat'].upper()}")
    ap(f"      {d2['raison']}")
    kns = d2["k_nominal_strates"]        # ADR-0028 §1 bis.1 pt 10 ; annexe D.5, bloc 6 (lot CRITERE, C-8)
    ap(f"      entrées (ADR-0028 §1 bis.1 pt 10) : « R1 discrimine » = {d2['r1_discrimine']} (bloc 3"
       + (f" ; strate(s) : {', '.join(d2['rejette'])}" if d2["rejette"] else "") + ") ; k_eff "
       + (f"≤ {d2['k_eff']} (borne supérieure)" if kp.get("k_eff_is_upper_bound")
          else f"= {_fmt_dec(d2['k_eff'])}")
       + f" ; k nominal du segment (hôtes) = {d2['k_nominal']} ; k nominal_s (flux du "
       "pool de la strate) : " + (", ".join(f"« {s} » = {k}" for s, k in kns.items()) or "aucune strate")
       + (" — comparaison hétérogène déclarée" if any(k != d2["k_nominal"] for k in kns.values()) else "")
       + " ; strate poolée hors des entrées")
    loc = d2.get("localisation_inter_clusters")
    if loc:
        ap(f"      localisation ({loc['note']}) — consomme la matrice de co-écarts M1b :")
        for st, rows in loc["par_strate"].items():
            top = rows[:5]
            ap(f"        strate « {st} » : "
               + (", ".join(f"{r['pair']}(n11={r['n11']})" for r in top) if top
                  else "aucune paire inter-clusters à co-écart"))

    # ── Sensibilité (ADR-0025 déc. 4 ; ADR-0028 D2 pt 7, §1 bis.1 pt 9) : avec une plage seulement (C-6) ──
    if ranges:
        pools_i, pool_i, _r = analysis_pools(dans_seg[0], readings, pool)   # D1 mécanique sur la variante
        r1_i = compute_r1(dans_seg[0], readings, pool_i, w, sigma_by_class, sigma_class_of_flux, tau,
                          seuil_hist, n_min, pools_i)
        sc = params["strate_calendar"]
        we, jours = sc.get("kind") == "weekend_utc", set(sc.get("stress_weekdays", ()))
        ap("\n[SENSIBILITÉ] " + ("PLAGE D'EXCLUSION INCLUSE" if len(ranges) == 1 else    # SENS-PLAGES-1
                                f"{len(ranges)} PLAGES D'EXCLUSION INCLUSES") + " — ADR-0025 déc. 4 ; ADR-0028 D2 "
           "pt 7 (liste fermée), §1 bis.1 pt 9 : hors décision")
        ap("  variante « exclue » = principale (blocs 1-6) ; variante « incluse » = sensibilité — biaisée "
           "vers le haut par construction ; documente l'exclusion D5 ; pas un estimateur alternatif")
        ap("  motif de l'exclusion (harnais dégradé, ADR-0025) : causalité non établie")
        ap("  assiette : fenêtres du segment (bloc 1), dédoublonnées (last-wins) ; R1 seul par variante, "
           "pool d'analyse D1 de la variante ; ni L&M ni R2 ; écart de z = z(incluse) − z(exclue)")
        ap("  comptes de pertes par type d'enregistrement, retirés par la plage, plage par plage puis union "
           "(SHOGEN-DP-JOURNAL-LOSS-1, ADR-0028 annexe D.5 ; repris du bloc 1, sans second calcul) :")
        for t in pertes:
            ap(f"    {t}")
        ws_seg = build_window_strate(dans_seg[0])           # SHOGEN-SENS-PERTES-2 : assiette du segment
        for a, b in ranges:
            sa = fenetres_sautees(ws_tous, sc, w, (a, b + 1) if seg is None else (max(a, seg[0]),
                                                                                   min(b + 1, seg[1])))
            ab = Counter()
            for x, s in ws_seg.items():
                ab[s] += sum((x, f) not in reading_map for f in pools_i[s]) if a <= x <= b else 0
            ls = sorted({*strates, *sa})
            ap(f"    [{a} ; {b}] pertes du journal dans la plage : fenêtres de grille sans marqueur "
               + ", ".join(f"{s} {sa.get(s, 0)}" for s in ls) + " ; lectures absentes des fenêtres à marqueur "
               "(pool D1 de la variante incluse) " + ", ".join(f"{s} {ab[s]}" for s in ls)
               + " — SHOGEN-SENS-PERTES-2")
        for st in (sorted({sc["calme"], sc["stress"]}) if we else [sc.get("strate", STRATE_DEFAUT)]):
            e, i = r1.get("strates", {}).get(st), r1_i.get("strates", {}).get(st)
            ap(_ligne_variante(st, "exclue (principale)", e))
            ap(_ligne_variante(st, "incluse (sensibilité)", i))
            if e is None or i is None or e["z"] is None or i["z"] is None:
                ap(f"  {st:8} écart de z : non calculable (z non publié ou strate absente d'une variante)")
            else:
                with localcontext() as ctx:
                    ctx.prec = DECIMAL_PREC
                    dz = +(i["z"] - e["z"])
                ap(f"  {st:8} écart de z = {_fmt_dec(dz)}")
            if e is not None and i is not None and pools[st] != pools_i[st]:
                ap(f"  {st:8} pool d'analyse D1 : exclue {pools[st]} ; incluse {pools_i[st]} (diffèrent)")
        if not (we and 0 < len(jours) < 7):
            ap("  couverture par week-end : non applicable ("
               + ("stress_weekdays sans borne de week-end)" if we else "calendrier mono-strate)"))
        else:
            ex, inc = (_week_ends(build_window_strate(m), sc) for m in (markers, dans_seg[0]))
            jrs = sorted(build_window_strate(dans_seg[0]))    # G2 C-5 : week-ends calendaires de l'assiette
            cal = _week_ends({d * 86400: sc["stress"] for d in range(jrs[0] // 86400, jrs[-1] // 86400 + 1)
                              if weekday_utc(d * 86400) in jours}, sc) if jrs else {}
            inc = {k: inc.get(k, 0) for k in sorted(set(inc) | set(cal))}
            plein = {k: len(range(-(-k[0] // w) * w, k[1], w)) for k in inc}
            ap(f"  couverture par week-end (fenêtres « {sc['stress']} », stress_weekdays = {sorted(jours)} "
               f"UTC ; w = {w} s de run_params ; durée = fenêtres × w) :"
               + ("" if inc else " aucun week-end"))
            for (a, b), n_i in sorted(inc.items()):
                n_e = ex.get((a, b), 0)
                ap(f"    week-end {_iso_utc(a)[:10]} [{a} ; {b}) : complet = {plein[a, b]} fenêtres = "
                   f"{_duree(plein[a, b] * w)} ; exclue {n_e} = {_duree(n_e * w)} ; incluse {n_i} = "
                   f"{_duree(n_i * w)} ; retirées par la plage {n_i - n_e}")
            tot = [sum(1 for k in inc if d.get(k, 0) == plein[k]) for d in (ex, inc)]
            par = [sum(1 for k in inc if 0 < d.get(k, 0) < plein[k]) for d in (ex, inc)]
            ap(f"    en totalité : exclue {tot[0]}, incluse {tot[1]} ; partiellement : exclue {par[0]}, "
               f"incluse {par[1]} ; retirés en totalité par la plage : "
               f"{sum(1 for k in inc if inc[k] and k not in ex)}")
            ap("    non couverts (0 fenêtre dans les deux variantes, entre la première et la dernière "
               f"fenêtre de l'assiette) : {sum(1 for k in inc if not inc[k])}")
    ap("=" * 78)
    return "\n".join(out)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="python -m shogen_s2.report")
    p.add_argument("journal_dir")
    p.add_argument("--exclude-window-start-range", nargs=2, type=int, action="append",
                   default=[], metavar=("FROM_EPOCH", "TO_EPOCH"),
                   help="plage FERMEE de window_start hors n, K, P_more (repetable, ADR-0025)")
    p.add_argument("--segment-from", type=int, metavar="T0_EPOCH", help="segment [T0 ; fin) (ADR-0028 D4)")
    fin = p.add_mutually_exclusive_group()
    fin.add_argument("--segment-to", type=int, metavar="T_FIN_EPOCH", help="fin exclue du segment")
    fin.add_argument("--segment-n-fixe", type=int, metavar="N",
                     help="fin = window_start de la N-ieme fenetre distincte >= T0, + w (ADR-0024)")
    args = p.parse_args(argv[1:])
    if (args.segment_from is None) != (args.segment_to is None and args.segment_n_fixe is None):
        p.error("segment : --segment-from avec --segment-to ou --segment-n-fixe (ADR-0028 D4)")
    neg = [x for x in [args.segment_from, args.segment_to, *sum(args.exclude_window_start_range, [])]
           if x is not None and x < 0]
    if neg:                    # avant l'API (ValueError, rc 1) : rc 2, rien sur stdout (SHOGEN-NEG-EPOCH-1)
        p.error(f"epoch negatif refuse {neg} (segment ou exclusion ; SHOGEN-NEG-EPOCH-1, ADR-0028 D5)")
    seg = None if args.segment_from is None else {
        "t0": args.segment_from, "t_fin": args.segment_to, "n_fixe": args.segment_n_fixe}
    d = args.journal_dir
    text = render_report(os.path.join(d, "control.jsonl"),
                         os.path.join(d, "journal.jsonl"),
                         exclude_ranges=args.exclude_window_start_range, segment=seg)
    # Émission UTF-8 explicite : la table porte la notation de doc 10 (P̂₀, p̂ᵢ…)
    # dont des diacritiques combinants qu'une console cp1252 (Windows) ne peut
    # encoder ; l'artefact recalculable est UTF-8, indépendant du code-page.
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
